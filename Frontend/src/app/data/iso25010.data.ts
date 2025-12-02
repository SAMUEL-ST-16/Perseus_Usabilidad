import { ISO25010Info } from '../models/requirement.model';

/**
 * Información detallada sobre ISO 25010 y sus subcaracterísticas de usabilidad
 */

export const ISO25010_SECURITY_SUBCHARACTERISTICS: ISO25010Info[] = [
  {
    name: 'Operabilidad',
    description: 'Grado en que un producto tiene atributos que hacen que sea fácil de operar y controlar.',
    examples: [
      'Navegación intuitiva y clara',
      'Botones y controles bien ubicados',
      'Deshacer y rehacer acciones',
      'Atajos de teclado útiles'
    ],
    icon: 'operability-icon.svg'
  },
  {
    name: 'Aprendizabilidad',
    description: 'Grado en que un producto puede ser usado por usuarios para lograr objetivos de aprendizaje con efectividad, eficiencia y satisfacción.',
    examples: [
      'Tutoriales y guías paso a paso',
      'Tooltips y mensajes de ayuda contextuales',
      'Curva de aprendizaje suave',
      'Documentación clara y ejemplos prácticos'
    ],
    icon: 'learnability-icon.svg'
  },
  {
    name: 'Involucración del usuario',
    description: 'Grado en que la interfaz presenta funciones y contenido que motivan y satisfacen al usuario.',
    examples: [
      'Diseño atractivo y motivador',
      'Feedback visual inmediato',
      'Gamificación y recompensas',
      'Personalización de la interfaz'
    ],
    icon: 'engagement-icon.svg'
  },
  {
    name: 'Reconocibilidad de adecuación',
    description: 'Grado en que los usuarios pueden reconocer si un producto es adecuado para sus necesidades.',
    examples: [
      'Interfaz clara que muestra funciones principales',
      'Descripción de características accesible',
      'Demo o tour de funcionalidades',
      'Información sobre casos de uso'
    ],
    icon: 'appropriateness-icon.svg'
  },
  {
    name: 'Protección frente a errores de usuario',
    description: 'Grado en que el sistema protege a los usuarios de cometer errores.',
    examples: [
      'Validación de formularios en tiempo real',
      'Confirmaciones para acciones críticas',
      'Prevención de entradas incorrectas',
      'Mensajes de error claros y accionables'
    ],
    icon: 'error-protection-icon.svg'
  },
  {
    name: 'Inclusividad',
    description: 'Grado en que un producto puede ser usado por personas con la más amplia gama de características y capacidades.',
    examples: [
      'Soporte para lectores de pantalla',
      'Contraste de colores adecuado',
      'Navegación por teclado',
      'Tamaños de fuente ajustables'
    ],
    icon: 'inclusivity-icon.svg'
  },
  {
    name: 'Auto descriptividad',
    description: 'Grado en que la interfaz proporciona información suficiente para que el usuario entienda cómo usarla sin consultar documentación externa.',
    examples: [
      'Etiquetas claras en todos los elementos',
      'Iconos auto-explicativos',
      'Mensajes informativos contextuales',
      'Instrucciones integradas en la interfaz'
    ],
    icon: 'self-descriptiveness-icon.svg'
  },
  {
    name: 'Asistencia al usuario',
    description: 'Grado en que el producto proporciona ayuda cuando el usuario la necesita.',
    examples: [
      'Sistema de ayuda integrado',
      'FAQs y guías de usuario',
      'Chat de soporte en vivo',
      'Videos tutoriales y tooltips'
    ],
    icon: 'user-assistance-icon.svg'
  }
];

export const ISO25010_OVERVIEW = {
  title: 'ISO/IEC 25010 - Calidad de Producto de Software',
  description: `
    La norma ISO/IEC 25010 es un estándar internacional que define un modelo de calidad
    para productos de software y sistemas informáticos. Esta norma es parte de la familia
    SQuaRE (System and Software Quality Requirements and Evaluation).
  `,
  securityDescription: `
    La característica de Usabilidad en ISO/IEC 25010:2023 se enfoca en el grado en que un producto
    puede ser usado por usuarios específicos para lograr objetivos específicos con efectividad,
    eficiencia y satisfacción en un contexto de uso específico. Se divide en 8 subcaracterísticas.
  `,
  benefits: [
    'Estandarización de requisitos de usabilidad',
    'Mejora en la experiencia de usuario',
    'Facilita la evaluación y comparación de productos',
    'Reduce la curva de aprendizaje desde el diseño',
    'Aumenta la satisfacción y adopción del usuario'
  ],
  reference: 'ISO/IEC 25010:2023 - Systems and software engineering — Systems and software Quality Requirements and Evaluation (SQuaRE) — System and software quality models'
};
