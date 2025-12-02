/**
 * Modelos TypeScript para la aplicación Perseus
 * Basados en las respuestas del backend FastAPI
 */

// Subcaracterísticas de Usabilidad ISO 25010:2023
export enum UsabilitySubcharacteristic {
  OPERABILIDAD = 'Operabilidad',
  APRENDIZABILIDAD = 'Aprendizabilidad',
  INVOLUCRACION = 'Involucración del usuario',
  RECONOCIBILIDAD = 'Reconocibilidad de adecuación',
  PROTECCION_ERRORES = 'Protección frente a errores de usuario',
  INCLUSIVIDAD = 'Inclusividad',
  AUTO_DESCRIPTIVIDAD = 'Auto descriptividad',
  ASISTENCIA = 'Asistencia al usuario'
}

// Información detallada de cada subcaracterística
export interface ISO25010Info {
  name: string;
  description: string;
  examples: string[];
  icon?: string; // Placeholder para icono
}

// Requisito de usabilidad procesado
export interface UsabilityRequirement {
  comment: string;
  subcharacteristic: string;
  description: string;
  binary_score?: number;
  multiclass_score?: number;
}

// Estadísticas de procesamiento (para Play Store URL)
export interface ProcessingStats {
  comments_processed: number;
  requirements_found: number;
  total_requirements_detected: number;
  success_rate: number;
  target: number;
}

// Respuesta del endpoint de comentario único
export interface SingleCommentResponse {
  // El backend retorna un PDF directamente
  pdf: Blob;
}

// Respuesta del endpoint de CSV
export interface CSVResponse {
  // El backend retorna un PDF directamente
  pdf: Blob;
}

// Respuesta del endpoint de Play Store
export interface PlayStoreResponse {
  // El backend retorna un PDF directamente
  pdf: Blob;
}

// Request para comentario único
export interface SingleCommentRequest {
  comment: string;
}

// Request para Play Store URL
export interface PlayStoreURLRequest {
  url: string;
}

// Estado de procesamiento
export interface ProcessingState {
  loading: boolean;
  progress?: number;
  message?: string;
  error?: string;
  results?: ProcessingResponse;
  showResults?: boolean;
  pdfBlob?: Blob;
  pdfFileName?: string;
}

// ============ NUEVOS MODELOS PARA VISUALIZACIÓN DE RESULTADOS ============

// Resultado individual de requisito (JSON del backend)
export interface RequirementResult {
  comment: string;
  is_requirement: boolean;
  subcharacteristic: string | null;
  description: string | null;
  binary_score: number;
  multiclass_score: number | null;
}

// Respuesta completa del procesamiento (JSON del backend)
export interface ProcessingResponse {
  total_comments: number;
  valid_requirements: number;
  requirements: RequirementResult[];
  processing_time_ms: number;
  source_type: 'single' | 'csv' | 'playstore';
}

// Estadísticas por subcaracterística para gráficos
export interface SubcharacteristicStats {
  name: string;
  count: number;
  percentage: number;
  color: string;
  icon: string;
}

// Colores para cada subcaracterística
export const SUBCHARACTERISTIC_COLORS: Record<string, string> = {
  'Operabilidad': '#667eea',
  'Aprendizabilidad': '#f093fb',
  'Involucración del usuario': '#4facfe',
  'Reconocibilidad de adecuación': '#43e97b',
  'Protección frente a errores de usuario': '#fa709a',
  'Inclusividad': '#feca57',
  'Auto descriptividad': '#38b2ac',
  'Asistencia al usuario': '#ed64a6'
};

// Iconos SVG para cada subcaracterística (SVG paths)
export const SUBCHARACTERISTIC_ICONS: Record<string, string> = {
  'Operabilidad': '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4" />',
  'Aprendizabilidad': '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />',
  'Involucración del usuario': '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />',
  'Reconocibilidad de adecuación': '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />',
  'Protección frente a errores de usuario': '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />',
  'Inclusividad': '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />',
  'Auto descriptividad': '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />',
  'Asistencia al usuario': '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 5.636l-3.536 3.536m0 5.656l3.536 3.536M9.172 9.172L5.636 5.636m3.536 9.192l-3.536 3.536M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-5 0a4 4 0 11-8 0 4 4 0 018 0z" />'
};
