import { ProcessingResponse } from '../models/requirement.model';

/**
 * Datos de ejemplo para demostración del dashboard
 * Simula resultados de un procesamiento real
 * Actualizado para reflejar requisitos de USABILIDAD según ISO/IEC 25010:2023
 */

export const MOCK_SINGLE_COMMENT_RESULT: ProcessingResponse = {
  total_comments: 1,
  valid_requirements: 1,
  processing_time_ms: 1234.56,
  source_type: 'single',
  requirements: [
    {
      comment: 'La aplicación debería tener un tutorial interactivo al inicio',
      is_requirement: true,
      subcharacteristic: 'Aprendizabilidad',
      description: 'El sistema debe implementar un tutorial interactivo paso a paso que guíe a los nuevos usuarios a través de las funcionalidades principales durante su primera experiencia.',
      binary_score: 0.9523,
      multiclass_score: 0.8756
    }
  ]
};

export const MOCK_CSV_RESULT: ProcessingResponse = {
  total_comments: 25,
  valid_requirements: 12,
  processing_time_ms: 5234.78,
  source_type: 'csv',
  requirements: [
    {
      comment: 'Los botones son difíciles de encontrar en la pantalla',
      is_requirement: true,
      subcharacteristic: 'Operabilidad',
      description: 'El sistema debe mejorar la ubicación y visibilidad de los botones principales, asegurando que sean fácilmente identificables y accesibles para los usuarios.',
      binary_score: 0.9234,
      multiclass_score: 0.8923
    },
    {
      comment: 'No hay ayuda disponible cuando la necesito',
      is_requirement: true,
      subcharacteristic: 'Asistencia al usuario',
      description: 'El sistema debe proporcionar ayuda contextual accesible en todo momento, incluyendo tooltips, FAQs y un sistema de ayuda integrado.',
      binary_score: 0.8945,
      multiclass_score: 0.8234
    },
    {
      comment: 'La app es aburrida y no me motiva a usarla',
      is_requirement: true,
      subcharacteristic: 'Involucración del usuario',
      description: 'El sistema debe incorporar elementos de diseño atractivos, feedback visual inmediato y posibles elementos de gamificación para aumentar el compromiso del usuario.',
      binary_score: 0.9123,
      multiclass_score: 0.8567
    },
    {
      comment: 'No entiendo para qué sirve cada función',
      is_requirement: true,
      subcharacteristic: 'Reconocibilidad de adecuación',
      description: 'El sistema debe proporcionar descripciones claras de cada funcionalidad, permitiendo a los usuarios entender rápidamente si satisface sus necesidades.',
      binary_score: 0.8834,
      multiclass_score: 0.8112
    },
    {
      comment: 'Borré algo importante sin querer',
      is_requirement: true,
      subcharacteristic: 'Protección frente a errores de usuario',
      description: 'El sistema debe implementar confirmaciones para acciones críticas y proporcionar opciones de deshacer para prevenir pérdida accidental de datos.',
      binary_score: 0.9456,
      multiclass_score: 0.9012
    },
    {
      comment: 'No puedo usar la app con lector de pantalla',
      is_requirement: true,
      subcharacteristic: 'Inclusividad',
      description: 'El sistema debe ser compatible con lectores de pantalla y cumplir con las pautas WCAG para garantizar accesibilidad a usuarios con discapacidades visuales.',
      binary_score: 0.8923,
      multiclass_score: 0.8456
    },
    {
      comment: 'Los iconos no son claros',
      is_requirement: true,
      subcharacteristic: 'Auto descriptividad',
      description: 'El sistema debe utilizar iconos auto-explicativos acompañados de etiquetas textuales que permitan a los usuarios entender su función sin consultar documentación externa.',
      binary_score: 0.9012,
      multiclass_score: 0.8734
    },
    {
      comment: 'Es muy difícil aprender a usar esta aplicación',
      is_requirement: true,
      subcharacteristic: 'Aprendizabilidad',
      description: 'El sistema debe reducir la curva de aprendizaje mediante tutoriales, tooltips contextuales y una interfaz intuitiva que facilite el aprendizaje progresivo.',
      binary_score: 0.8767,
      multiclass_score: 0.8345
    },
    {
      comment: 'El menú es confuso y no encuentro las opciones',
      is_requirement: true,
      subcharacteristic: 'Operabilidad',
      description: 'El sistema debe reestructurar el menú de navegación para que sea más intuitivo, organizando las opciones de manera lógica y fácil de entender.',
      binary_score: 0.9234,
      multiclass_score: 0.8901
    },
    {
      comment: 'No hay forma de contactar soporte',
      is_requirement: true,
      subcharacteristic: 'Asistencia al usuario',
      description: 'El sistema debe proporcionar múltiples canales de soporte accesibles, incluyendo chat en vivo, correo electrónico y un centro de ayuda completo.',
      binary_score: 0.8912,
      multiclass_score: 0.8234
    },
    {
      comment: 'La interfaz se ve anticuada',
      is_requirement: true,
      subcharacteristic: 'Involucración del usuario',
      description: 'El sistema debe modernizar su interfaz visual con un diseño contemporáneo que sea estéticamente agradable y motive a los usuarios a interactuar con la aplicación.',
      binary_score: 0.9123,
      multiclass_score: 0.8678
    },
    {
      comment: 'El texto es muy pequeño y no puedo leerlo',
      is_requirement: true,
      subcharacteristic: 'Inclusividad',
      description: 'El sistema debe permitir ajustar el tamaño de fuente y proporcionar un tamaño de texto base adecuado que sea legible para usuarios con diferentes capacidades visuales.',
      binary_score: 0.9345,
      multiclass_score: 0.8923
    }
  ]
};

export const MOCK_PLAYSTORE_RESULT: ProcessingResponse = {
  total_comments: 150,
  valid_requirements: 18,
  processing_time_ms: 12456.89,
  source_type: 'playstore',
  requirements: [
    {
      comment: 'Necesito un tutorial para aprender a usar la app',
      is_requirement: true,
      subcharacteristic: 'Aprendizabilidad',
      description: 'El sistema debe implementar un tutorial interactivo inicial que explique las funciones principales de manera clara y progresiva.',
      binary_score: 0.9423,
      multiclass_score: 0.8934
    },
    {
      comment: 'Los botones están mal ubicados',
      is_requirement: true,
      subcharacteristic: 'Operabilidad',
      description: 'El sistema debe reorganizar la ubicación de los botones siguiendo principios de diseño de interfaz, colocándolos en posiciones predecibles y fácilmente accesibles.',
      binary_score: 0.9567,
      multiclass_score: 0.9123
    },
    {
      comment: 'No sé si esta app me sirve',
      is_requirement: true,
      subcharacteristic: 'Reconocibilidad de adecuación',
      description: 'El sistema debe proporcionar una descripción clara de sus capacidades y casos de uso en la pantalla inicial, ayudando a los usuarios a determinar su adecuación.',
      binary_score: 0.8923,
      multiclass_score: 0.8456
    },
    {
      comment: 'Perdí datos importantes porque no me avisó',
      is_requirement: true,
      subcharacteristic: 'Protección frente a errores de usuario',
      description: 'El sistema debe implementar diálogos de confirmación antes de realizar acciones destructivas y proporcionar funcionalidad de deshacer.',
      binary_score: 0.9012,
      multiclass_score: 0.8734
    },
    {
      comment: 'No funciona bien con mi lector de pantalla',
      is_requirement: true,
      subcharacteristic: 'Inclusividad',
      description: 'El sistema debe ser totalmente compatible con tecnologías asistivas, implementando etiquetas ARIA y navegación por teclado adecuada.',
      binary_score: 0.9234,
      multiclass_score: 0.8867
    },
    {
      comment: 'Los iconos no tienen etiquetas',
      is_requirement: true,
      subcharacteristic: 'Auto descriptividad',
      description: 'El sistema debe agregar etiquetas textuales a todos los iconos, haciendo la interfaz auto-explicativa sin necesidad de documentación externa.',
      binary_score: 0.9123,
      multiclass_score: 0.8678
    },
    {
      comment: 'No hay ayuda cuando tengo dudas',
      is_requirement: true,
      subcharacteristic: 'Asistencia al usuario',
      description: 'El sistema debe proporcionar un sistema de ayuda contextual accesible desde cualquier pantalla, con respuestas a preguntas frecuentes.',
      binary_score: 0.9456,
      multiclass_score: 0.9012
    },
    {
      comment: 'El diseño no me motiva a usar la app',
      is_requirement: true,
      subcharacteristic: 'Involucración del usuario',
      description: 'El sistema debe mejorar el diseño visual para hacerlo más atractivo, implementando elementos que generen satisfacción y compromiso del usuario.',
      binary_score: 0.9234,
      multiclass_score: 0.8901
    },
    {
      comment: 'Es muy complicado hacer tareas simples',
      is_requirement: true,
      subcharacteristic: 'Operabilidad',
      description: 'El sistema debe simplificar los flujos de trabajo para tareas comunes, reduciendo el número de pasos necesarios para completar acciones básicas.',
      binary_score: 0.8834,
      multiclass_score: 0.8345
    },
    {
      comment: 'Tardé mucho en entender cómo funciona',
      is_requirement: true,
      subcharacteristic: 'Aprendizabilidad',
      description: 'El sistema debe mejorar la curva de aprendizaje mediante onboarding progresivo, tooltips contextuales y documentación accesible.',
      binary_score: 0.9123,
      multiclass_score: 0.8756
    },
    {
      comment: 'No entiendo para qué sirven las funciones',
      is_requirement: true,
      subcharacteristic: 'Reconocibilidad de adecuación',
      description: 'El sistema debe proporcionar descripciones claras de cada funcionalidad, permitiendo a los usuarios reconocer rápidamente su utilidad.',
      binary_score: 0.9345,
      multiclass_score: 0.8923
    },
    {
      comment: 'Borré un archivo importante sin confirmación',
      is_requirement: true,
      subcharacteristic: 'Protección frente a errores de usuario',
      description: 'El sistema debe solicitar confirmación explícita antes de eliminar archivos y proporcionar papelera de reciclaje para recuperación.',
      binary_score: 0.8912,
      multiclass_score: 0.8567
    },
    {
      comment: 'El contraste de colores es malo',
      is_requirement: true,
      subcharacteristic: 'Inclusividad',
      description: 'El sistema debe mejorar el contraste de colores para cumplir con WCAG AA, facilitando la lectura para usuarios con deficiencias visuales.',
      binary_score: 0.9234,
      multiclass_score: 0.8901
    },
    {
      comment: 'Los mensajes de error no son claros',
      is_requirement: true,
      subcharacteristic: 'Auto descriptividad',
      description: 'El sistema debe proporcionar mensajes de error descriptivos que expliquen qué salió mal y cómo solucionarlo, sin necesidad de consultar documentación.',
      binary_score: 0.9012,
      multiclass_score: 0.8678
    },
    {
      comment: 'No encuentro el centro de ayuda',
      is_requirement: true,
      subcharacteristic: 'Asistencia al usuario',
      description: 'El sistema debe hacer más visible y accesible el centro de ayuda, colocándolo en ubicaciones predecibles de la interfaz.',
      binary_score: 0.9456,
      multiclass_score: 0.9123
    },
    {
      comment: 'La app es poco intuitiva',
      is_requirement: true,
      subcharacteristic: 'Operabilidad',
      description: 'El sistema debe rediseñar la interfaz siguiendo convenciones estándar de diseño para hacerla más intuitiva y predecible.',
      binary_score: 0.9234,
      multiclass_score: 0.8834
    },
    {
      comment: 'No hay feedback visual cuando hago algo',
      is_requirement: true,
      subcharacteristic: 'Involucración del usuario',
      description: 'El sistema debe proporcionar feedback visual inmediato para todas las acciones del usuario, confirmando que sus interacciones fueron registradas.',
      binary_score: 0.9123,
      multiclass_score: 0.8756
    },
    {
      comment: 'No puedo navegar con el teclado',
      is_requirement: true,
      subcharacteristic: 'Inclusividad',
      description: 'El sistema debe implementar navegación completa por teclado, permitiendo a usuarios con limitaciones motoras acceder a todas las funcionalidades.',
      binary_score: 0.9345,
      multiclass_score: 0.8912
    }
  ]
};
