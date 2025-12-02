"""
Description Service
Generates human-readable descriptions for security requirements using AI
"""

from typing import Dict, Optional
import os
from openai import OpenAI
from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class DescriptionService:
    """
    Service for generating requirement descriptions using OpenAI/Groq

    Uses LLM to generate detailed, context-aware requirement descriptions
    based on the original comment and detected security subcharacteristic.
    """

    # Subcharacteristic definitions (ISO 25010)
    SUBCHARACTERISTIC_DEFINITIONS: Dict[str, str] = {
        "Autenticidad": "Verificar que usuarios, entidades o recursos sean quienes dicen ser",
        "Confidencialidad": "Proteger información contra accesos no autorizados",
        "Integridad": "Prevenir modificaciones no autorizadas de datos",
        "Responsabilidad": "Rastrear acciones de manera única a una entidad",
        "No-Repudio": "Probar que una acción ocurrió sin posibilidad de negación",
        "Resistencia": "Mantener funcionalidad ante ataques o fallos"
    }

    def __init__(self):
        """Initialize description service with AI client"""
        logger.info("Initializing AI-powered Description Service")

        # Initialize OpenAI client (works with OpenAI and Groq)
        self.openai_client = None
        self.use_ai = False
        self.provider = None
        self.model = None

        # Prioritize based on PROVIDER setting
        provider = settings.PROVIDER.lower()

        if provider == "groq" and settings.GROQ_API_KEY:
            # Try Groq first (prioritized)
            try:
                self.openai_client = OpenAI(
                    api_key=settings.GROQ_API_KEY,
                    base_url="https://api.groq.com/openai/v1"
                )
                self.use_ai = True
                self.provider = "groq"
                self.model = settings.GROQ_MODEL_NAME
                logger.info(f"✓ Groq client initialized with model: {self.model}")
            except Exception as e:
                logger.warning(f"Failed to initialize Groq client: {e}")

        elif provider == "openai" and settings.OPENAI_API_KEY:
            # Try OpenAI if specified
            try:
                self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
                self.use_ai = True
                self.provider = "openai"
                self.model = "gpt-4o-mini"
                logger.info(f"✓ OpenAI client initialized with model: {self.model}")
            except Exception as e:
                logger.warning(f"Failed to initialize OpenAI client: {e}")

        # Fallback to any available provider
        if not self.use_ai:
            if settings.GROQ_API_KEY:
                try:
                    self.openai_client = OpenAI(
                        api_key=settings.GROQ_API_KEY,
                        base_url="https://api.groq.com/openai/v1"
                    )
                    self.use_ai = True
                    self.provider = "groq"
                    self.model = settings.GROQ_MODEL_NAME
                    logger.info(f"✓ Groq client initialized (fallback) with model: {self.model}")
                except Exception as e:
                    logger.warning(f"Failed to initialize Groq client: {e}")

            elif settings.OPENAI_API_KEY:
                try:
                    self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
                    self.use_ai = True
                    self.provider = "openai"
                    self.model = "gpt-4o-mini"
                    logger.info(f"✓ OpenAI client initialized (fallback) with model: {self.model}")
                except Exception as e:
                    logger.warning(f"Failed to initialize OpenAI client: {e}")

        if not self.use_ai:
            logger.warning("No AI client available - will use template-based descriptions")

    def _generate_with_ai(
        self,
        comment: str,
        subcharacteristic: str
    ) -> Optional[str]:
        """
        Generate description using AI (OpenAI/Groq)

        Args:
            comment: Original user comment
            subcharacteristic: Detected security subcharacteristic

        Returns:
            Generated description or None if failed
        """
        try:
            subchar_definition = self.SUBCHARACTERISTIC_DEFINITIONS.get(
                subcharacteristic,
                "Requisito de seguridad"
            )

            # Build prompt
            prompt = f"""Eres un experto en ingeniería de requisitos de software y seguridad ISO 25010.

Comentario del usuario: "{comment}"

Subcaracterística de seguridad detectada: {subcharacteristic}
Definición: {subchar_definition}

Tarea: Genera UNA descripción formal de requisito de seguridad basada en el comentario del usuario.

Requisitos:
- Escribe en tercera persona (El sistema debe...)
- Sé específico sobre QUÉ debe hacer el sistema
- Incluye elementos del comentario original
- Máximo 2-3 oraciones
- Enfócate en {subcharacteristic}
- Redacción profesional y técnica

IMPORTANTE: Devuelve SOLO la descripción del requisito, sin explicaciones adicionales."""

            # Call API with configured model
            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Eres un experto en ingeniería de requisitos de seguridad."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=200
            )

            description = response.choices[0].message.content.strip()

            logger.info(f"✓ Groq generated description for '{comment[:50]}...': {description[:100]}...")
            return description

        except Exception as e:
            logger.error(f"❌ AI description generation failed for '{comment[:50]}...': {e}")
            return None

    def _generate_with_template(
        self,
        comment: str,
        subcharacteristic: str
    ) -> str:
        """
        Generate description using templates (fallback)

        Args:
            comment: Original user comment
            subcharacteristic: Security subcharacteristic

        Returns:
            Template-based description
        """
        templates = {
            "Autenticidad": "El sistema debe implementar mecanismos de autenticación robustos para verificar la identidad de usuarios y entidades, asegurando que sean quienes afirman ser.",
            "Confidencialidad": "El sistema debe proteger la información sensible mediante cifrado y controles de acceso apropiados para prevenir divulgación no autorizada.",
            "Integridad": "El sistema debe garantizar la integridad de los datos mediante mecanismos que detecten y prevengan modificaciones no autorizadas.",
            "Responsabilidad": "El sistema debe mantener registros de auditoría detallados para rastrear las acciones de manera única y asegurar la responsabilidad.",
            "No-Repudio": "El sistema debe implementar mecanismos de no repudio que permitan probar la ocurrencia de acciones sin posibilidad de negación posterior.",
            "Resistencia": "El sistema debe ser resistente ante ataques y fallos mediante la implementación de controles de seguridad y mecanismos de recuperación."
        }

        return templates.get(
            subcharacteristic,
            "El sistema debe implementar medidas de seguridad apropiadas según las mejores prácticas de la industria."
        )

    def generate_description(
        self,
        comment: str,
        subcharacteristic: str
    ) -> str:
        """
        Generate a formal description for a security requirement

        Uses AI if available, falls back to templates otherwise.

        Args:
            comment: Original user comment
            subcharacteristic: Detected security subcharacteristic

        Returns:
            Generated description in formal requirement language
        """
        # Try AI generation first
        if self.use_ai:
            logger.info(f"🤖 Generating AI description ({self.provider}) for: {subcharacteristic}")
            ai_description = self._generate_with_ai(comment, subcharacteristic)
            if ai_description:
                return ai_description

        # Fallback to template
        logger.warning(f"⚠️  Using template-based description for: {subcharacteristic}")
        return self._generate_with_template(comment, subcharacteristic)


# Global service instance
description_service = DescriptionService()
