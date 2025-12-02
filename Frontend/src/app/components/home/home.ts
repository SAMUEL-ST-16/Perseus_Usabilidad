import { Component, OnInit, inject, signal, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { ApiService } from '../../services/api.service';
import { ProcessingState, ProcessingResponse } from '../../models/requirement.model';
import { ResultsDashboardComponent } from '../results-dashboard/results-dashboard';
import {
  MOCK_SINGLE_COMMENT_RESULT,
  MOCK_CSV_RESULT,
  MOCK_PLAYSTORE_RESULT
} from '../../data/mock-results.data';

/**
 * Componente Home - Página principal con diseño v0.app
 * Diseño profesional y limpio adaptado de v0.app
 * Incluye: Header, Hero, Input Cards, Usability Characteristics, Demo Mode, Light Theme Only
 */
@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, FormsModule, ResultsDashboardComponent],
  templateUrl: './home.html',
  styleUrl: './home.css'
})
export class HomeComponent implements OnInit {
  private apiService = inject(ApiService);
  private router = inject(Router);

  ngOnInit() {
    // Forzar tema light
    document.documentElement.classList.remove('dark');
  }

  // ==================== ESTADO ====================
  // Señales para el estado de cada funcionalidad
  singleCommentState = signal<ProcessingState>({ loading: false });
  csvState = signal<ProcessingState>({ loading: false });
  playStoreState = signal<ProcessingState>({ loading: false });

  // Datos de formularios
  singleComment = signal<string>('');
  csvFile = signal<File | null>(null);
  csvFileName = signal<string>('');
  playStoreURL = signal<string>('');

  // Modo demostración activado/desactivado
  demoMode = signal<boolean>(false);

  // Característica expandida en la sección de usability characteristics
  expandedCharacteristic = signal<string | null>('');

  // ==================== VALIDACIÓN ====================
  readonly MIN_COMMENT_LENGTH = 10;
  readonly MIN_URL_LENGTH = 30;

  // ==================== DATOS DE CARACTERÍSTICAS ====================
  usabilityCharacteristics = [
    {
      id: 'chart1',
      name: 'Operabilidad',
      icon: 'cursor-click',
      color: 'chart1',
      description: 'Grado en que un producto tiene atributos que hacen que sea fácil de operar y controlar.',
      details: [
        'Navegación intuitiva y clara',
        'Botones y controles bien ubicados',
        'Deshacer y rehacer acciones',
        'Atajos de teclado útiles'
      ],
      examples: 'Los botones están mal ubicados / No puedo encontrar cómo hacer X'
    },
    {
      id: 'chart2',
      name: 'Aprendizabilidad',
      icon: 'academic-cap',
      color: 'chart2',
      description: 'Grado en que un producto puede ser usado por usuarios para lograr objetivos de aprendizaje con efectividad, eficiencia y satisfacción.',
      details: [
        'Tutoriales y guías paso a paso',
        'Tooltips y mensajes de ayuda contextuales',
        'Curva de aprendizaje suave',
        'Documentación clara y ejemplos prácticos'
      ],
      examples: 'Es muy difícil aprender a usar esta app / No hay tutoriales claros'
    },
    {
      id: 'chart3',
      name: 'Involucración del usuario',
      icon: 'heart',
      color: 'chart3',
      description: 'Grado en que la interfaz presenta funciones y contenido que motivan y satisfacen al usuario.',
      details: [
        'Diseño atractivo y motivador',
        'Feedback visual inmediato',
        'Gamificación y recompensas',
        'Personalización de la interfaz'
      ],
      examples: 'La app es aburrida / No me motiva a usarla / Falta interacción'
    },
    {
      id: 'chart4',
      name: 'Reconocibilidad de adecuación',
      icon: 'eye',
      color: 'chart4',
      description: 'Grado en que los usuarios pueden reconocer si un producto es adecuado para sus necesidades.',
      details: [
        'Interfaz clara que muestra funciones principales',
        'Descripción de características accesible',
        'Demo o tour de funcionalidades',
        'Información sobre casos de uso'
      ],
      examples: 'No entiendo para qué sirve esta función / No sé si esta app me ayudará'
    },
    {
      id: 'chart5',
      name: 'Protección frente a errores de usuario',
      icon: 'shield-check',
      color: 'chart5',
      description: 'Grado en que el sistema protege a los usuarios de cometer errores.',
      details: [
        'Validación de formularios en tiempo real',
        'Confirmaciones para acciones críticas',
        'Prevención de entradas incorrectas',
        'Mensajes de error claros y accionables'
      ],
      examples: 'Borré algo sin querer / No me advirtió antes de eliminar'
    },
    {
      id: 'chart6',
      name: 'Inclusividad',
      icon: 'users',
      color: 'chart6',
      description: 'Grado en que un producto puede ser usado por personas con la más amplia gama de características y capacidades.',
      details: [
        'Soporte para lectores de pantalla',
        'Contraste de colores adecuado',
        'Navegación por teclado',
        'Tamaños de fuente ajustables'
      ],
      examples: 'No puedo leer el texto, es muy pequeño / No funciona con lector de pantalla'
    },
    {
      id: 'chart7',
      name: 'Auto descriptividad',
      icon: 'light-bulb',
      color: 'chart7',
      description: 'Grado en que la interfaz proporciona información suficiente para que el usuario entienda cómo usarla sin consultar documentación externa.',
      details: [
        'Etiquetas claras en todos los elementos',
        'Iconos auto-explicativos',
        'Mensajes informativos contextuales',
        'Instrucciones integradas en la interfaz'
      ],
      examples: 'No sé qué hace este botón / Los iconos no son claros'
    },
    {
      id: 'chart8',
      name: 'Asistencia al usuario',
      icon: 'support',
      color: 'chart8',
      description: 'Grado en que el producto proporciona ayuda cuando el usuario la necesita.',
      details: [
        'Sistema de ayuda integrado',
        'FAQs y guías de usuario',
        'Chat de soporte en vivo',
        'Videos tutoriales y tooltips'
      ],
      examples: 'No hay ayuda disponible / No puedo resolver mis dudas'
    }
  ];

  // ==================== COMPUTED ====================
  // Determina si hay resultados para mostrar
  hasResults = computed(() => {
    return this.singleCommentState().showResults ||
           this.csvState().showResults ||
           this.playStoreState().showResults;
  });

  // Obtiene los resultados actuales para mostrar
  currentResults = computed(() => {
    if (this.singleCommentState().showResults) {
      return this.singleCommentState().results;
    }
    if (this.csvState().showResults) {
      return this.csvState().results;
    }
    if (this.playStoreState().showResults) {
      return this.playStoreState().results;
    }
    return null;
  });

  // Obtiene el PDF blob actual
  currentPdfBlob = computed(() => {
    if (this.singleCommentState().showResults) {
      return this.singleCommentState().pdfBlob;
    }
    if (this.csvState().showResults) {
      return this.csvState().pdfBlob;
    }
    if (this.playStoreState().showResults) {
      return this.playStoreState().pdfBlob;
    }
    return null;
  });

  // Obtiene el nombre del archivo PDF actual
  currentPdfFileName = computed(() => {
    if (this.singleCommentState().showResults) {
      return this.singleCommentState().pdfFileName;
    }
    if (this.csvState().showResults) {
      return this.csvState().pdfFileName;
    }
    if (this.playStoreState().showResults) {
      return this.playStoreState().pdfFileName;
    }
    return 'requisitos_usabilidad.pdf';
  });

  // ==================== CARACTERÍSTICAS DE USABILIDAD ====================
  toggleCharacteristic(id: string): void {
    if (this.expandedCharacteristic() === id) {
      this.expandedCharacteristic.set(null);
    } else {
      this.expandedCharacteristic.set(id);
    }
  }

  // ==================== MODO DEMOSTRACIÓN ====================
  toggleDemoMode(): void {
    this.demoMode.set(!this.demoMode());
  }

  showDemoResults(type: 'single' | 'csv' | 'playstore'): void {
    // Limpiar resultados anteriores
    this.clearAllResults();

    // Mostrar resultados de demostración
    setTimeout(() => {
      switch (type) {
        case 'single':
          this.singleCommentState.set({
            loading: false,
            showResults: true,
            results: MOCK_SINGLE_COMMENT_RESULT,
            message: 'Resultados de demostración - Comentario único'
          });
          break;
        case 'csv':
          this.csvState.set({
            loading: false,
            showResults: true,
            results: MOCK_CSV_RESULT,
            message: 'Resultados de demostración - Archivo CSV'
          });
          break;
        case 'playstore':
          this.playStoreState.set({
            loading: false,
            showResults: true,
            results: MOCK_PLAYSTORE_RESULT,
            message: 'Resultados de demostración - Google Play Store'
          });
          break;
      }

      // Scroll al dashboard
      setTimeout(() => {
        const dashboard = document.querySelector('.results-dashboard');
        if (dashboard) {
          dashboard.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      }, 100);
    }, 500);
  }

  clearAllResults(): void {
    this.singleCommentState.set({ loading: false, showResults: false });
    this.csvState.set({ loading: false, showResults: false });
    this.playStoreState.set({ loading: false, showResults: false });
  }

  // ==================== FUNCIONALIDAD 1: COMENTARIO ÚNICO ====================
  onSingleCommentSubmit(): void {
    const comment = this.singleComment().trim();

    // Validación
    if (!comment || comment.length < this.MIN_COMMENT_LENGTH) {
      this.singleCommentState.set({
        loading: false,
        error: `El comentario debe tener al menos ${this.MIN_COMMENT_LENGTH} caracteres`
      });
      return;
    }

    // Limpiar resultados anteriores
    this.clearAllResults();

    // Iniciar procesamiento
    this.singleCommentState.set({
      loading: true,
      message: 'Analizando comentario con modelos BERT...',
      progress: 30
    });

    // Intentar obtener PDF + JSON (resultados reales)
    this.apiService.processSingleCommentWithResults(comment).subscribe({
      next: ({ pdf, results }) => {
        // Usar resultados reales del backend
        this.singleCommentState.set({
          loading: false,
          showResults: true,
          results: results, // Datos reales del backend
          pdfBlob: pdf,
          pdfFileName: 'requisito_individual.pdf',
          message: 'Análisis completado - Descarga el PDF desde el botón abajo'
        });

        // Scroll al dashboard
        setTimeout(() => {
          const dashboard = document.querySelector('.results-dashboard');
          if (dashboard) {
            dashboard.scrollIntoView({ behavior: 'smooth', block: 'start' });
          }
        }, 100);
      },
      error: (error) => {
        console.error('Error obteniendo resultados JSON, intentando solo PDF...', error);

        // Fallback: usar solo PDF con datos MOCK si el endpoint /analyze/* no existe
        this.apiService.processSingleComment(comment).subscribe({
          next: (pdfBlob) => {
            this.singleCommentState.set({
              loading: false,
              showResults: true,
              results: MOCK_SINGLE_COMMENT_RESULT, // Datos de demostración como fallback
              pdfBlob: pdfBlob,
              pdfFileName: 'requisito_individual.pdf',
              message: 'Análisis completado - Descarga el PDF desde el botón abajo (Mostrando datos de demostración)'
            });

            setTimeout(() => {
              const dashboard = document.querySelector('.results-dashboard');
              if (dashboard) {
                dashboard.scrollIntoView({ behavior: 'smooth', block: 'start' });
              }
            }, 100);
          },
          error: (pdfError) => {
            console.error('Error procesando comentario:', pdfError);
            this.singleCommentState.set({
              loading: false,
              error: this.getErrorMessage(pdfError)
            });
          }
        });
      }
    });
  }

  clearSingleComment(): void {
    this.singleComment.set('');
    this.singleCommentState.set({ loading: false, showResults: false });
  }

  // ==================== FUNCIONALIDAD 2: ARCHIVO CSV ====================
  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      const file = input.files[0];

      if (!file.name.endsWith('.csv')) {
        this.csvState.set({
          loading: false,
          error: 'El archivo debe ser un CSV (.csv)'
        });
        return;
      }

      this.csvFile.set(file);
      this.csvFileName.set(file.name);
      this.csvState.set({ loading: false, error: undefined });
    }
  }

  onCSVSubmit(): void {
    const file = this.csvFile();

    if (!file) {
      this.csvState.set({
        loading: false,
        error: 'Por favor selecciona un archivo CSV'
      });
      return;
    }

    // Limpiar resultados anteriores
    this.clearAllResults();

    this.csvState.set({
      loading: true,
      message: 'Procesando archivo CSV...',
      progress: 20
    });

    // Intentar obtener PDF + JSON (resultados reales)
    this.apiService.processCSVWithResults(file).subscribe({
      next: ({ pdf, results }) => {
        // Usar resultados reales del backend
        this.csvState.set({
          loading: false,
          showResults: true,
          results: results, // Datos reales del backend
          pdfBlob: pdf,
          pdfFileName: `requisitos_${file.name.replace('.csv', '')}.pdf`,
          message: 'Análisis completado - Descarga el PDF desde el botón abajo'
        });

        // Scroll al dashboard
        setTimeout(() => {
          const dashboard = document.querySelector('.results-dashboard');
          if (dashboard) {
            dashboard.scrollIntoView({ behavior: 'smooth', block: 'start' });
          }
        }, 100);
      },
      error: (error) => {
        console.error('Error obteniendo resultados JSON, intentando solo PDF...', error);

        // Fallback: usar solo PDF con datos MOCK si el endpoint /analyze/* no existe
        this.apiService.processCSVFile(file).subscribe({
          next: (pdfBlob) => {
            this.csvState.set({
              loading: false,
              showResults: true,
              results: MOCK_CSV_RESULT, // Datos de demostración como fallback
              pdfBlob: pdfBlob,
              pdfFileName: `requisitos_${file.name.replace('.csv', '')}.pdf`,
              message: 'Análisis completado - Descarga el PDF desde el botón abajo (Mostrando datos de demostración)'
            });

            setTimeout(() => {
              const dashboard = document.querySelector('.results-dashboard');
              if (dashboard) {
                dashboard.scrollIntoView({ behavior: 'smooth', block: 'start' });
              }
            }, 100);
          },
          error: (pdfError) => {
            console.error('Error procesando CSV:', pdfError);
            this.csvState.set({
              loading: false,
              error: this.getErrorMessage(pdfError)
            });
          }
        });
      }
    });
  }

  clearCSV(): void {
    this.csvFile.set(null);
    this.csvFileName.set('');
    this.csvState.set({ loading: false, showResults: false });
  }

  // ==================== FUNCIONALIDAD 3: GOOGLE PLAY STORE ====================
  onPlayStoreSubmit(): void {
    const url = this.playStoreURL().trim();

    // Validación
    if (!url || url.length < this.MIN_URL_LENGTH) {
      this.playStoreState.set({
        loading: false,
        error: 'Por favor ingresa una URL válida de Google Play Store'
      });
      return;
    }

    if (!url.includes('play.google.com') || !url.includes('id=')) {
      this.playStoreState.set({
        loading: false,
        error: 'La URL debe ser de Google Play Store y contener el ID de la app'
      });
      return;
    }

    // Limpiar resultados anteriores
    this.clearAllResults();

    this.playStoreState.set({
      loading: true,
      message: 'Extrayendo comentarios de Google Play Store...',
      progress: 10
    });

    const appId = url.split('id=')[1].split('&')[0];

    // Intentar obtener PDF + JSON (resultados reales)
    this.apiService.processPlayStoreWithResults(url).subscribe({
      next: ({ pdf, results }) => {
        // Usar resultados reales del backend
        this.playStoreState.set({
          loading: false,
          showResults: true,
          results: results, // Datos reales del backend
          pdfBlob: pdf,
          pdfFileName: `requisitos_${appId}.pdf`,
          message: 'Análisis completado - Descarga el PDF desde el botón abajo'
        });

        // Scroll al dashboard
        setTimeout(() => {
          const dashboard = document.querySelector('.results-dashboard');
          if (dashboard) {
            dashboard.scrollIntoView({ behavior: 'smooth', block: 'start' });
          }
        }, 100);
      },
      error: (error) => {
        console.error('Error obteniendo resultados JSON, intentando solo PDF...', error);

        // Fallback: usar solo PDF con datos MOCK si el endpoint /analyze/* no existe
        this.apiService.processPlayStoreURL(url).subscribe({
          next: (pdfBlob) => {
            this.playStoreState.set({
              loading: false,
              showResults: true,
              results: MOCK_PLAYSTORE_RESULT, // Datos de demostración como fallback
              pdfBlob: pdfBlob,
              pdfFileName: `requisitos_${appId}.pdf`,
              message: 'Análisis completado - Descarga el PDF desde el botón abajo (Mostrando datos de demostración)'
            });

            setTimeout(() => {
              const dashboard = document.querySelector('.results-dashboard');
              if (dashboard) {
                dashboard.scrollIntoView({ behavior: 'smooth', block: 'start' });
              }
            }, 100);
          },
          error: (pdfError) => {
            console.error('Error procesando Play Store URL:', pdfError);
            this.playStoreState.set({
              loading: false,
              error: this.getErrorMessage(pdfError)
            });
          }
        });
      }
    });
  }

  clearPlayStore(): void {
    this.playStoreURL.set('');
    this.playStoreState.set({ loading: false, showResults: false });
  }

  // ==================== UTILIDADES ====================
  getErrorMessage(error: any): string {
    if (error.error?.message) {
      return error.error.message;
    }
    if (error.message) {
      return error.message;
    }
    if (error.status === 0) {
      return 'No se pudo conectar con el servidor. Verifica que el backend esté ejecutándose.';
    }
    return 'Ocurrió un error inesperado. Por favor intenta de nuevo.';
  }
}
