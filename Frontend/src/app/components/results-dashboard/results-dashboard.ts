import { Component, Input, computed, Signal, signal, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  ProcessingResponse,
  RequirementResult,
  SubcharacteristicStats,
  SUBCHARACTERISTIC_COLORS,
  SUBCHARACTERISTIC_ICONS
} from '../../models/requirement.model';
import { ApiService } from '../../services/api.service';

/**
 * Dashboard de Results - Componente de visualización elegante de resultados
 * Muestra estadísticas, tablas y gráficos de los requisitos encontrados
 */
@Component({
  selector: 'app-results-dashboard',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './results-dashboard.html',
  styleUrl: './results-dashboard.css'
})
export class ResultsDashboardComponent {
  private apiService = inject(ApiService);

  @Input() results!: ProcessingResponse;
  @Input() pdfBlob?: Blob | null;
  @Input() pdfFileName?: string;

  // Constantes para usar en el template
  SUBCHARACTERISTIC_COLORS = SUBCHARACTERISTIC_COLORS;
  SUBCHARACTERISTIC_ICONS = SUBCHARACTERISTIC_ICONS;

  // Tab activo para cambiar entre vista de tabla y estadísticas
  activeTab = signal<'table' | 'stats'>('table');

  // Estadísticas computadas por subcaracterística
  subcharacteristicStats = computed(() => {
    if (!this.results || !this.results.requirements) {
      return [];
    }

    // Contar requisitos por subcaracterística
    const counts: Record<string, number> = {};
    const validReqs = this.results.requirements.filter(r => r.is_requirement);

    validReqs.forEach(req => {
      if (req.subcharacteristic) {
        counts[req.subcharacteristic] = (counts[req.subcharacteristic] || 0) + 1;
      }
    });

    // Convertir a array de estadísticas
    const stats: SubcharacteristicStats[] = Object.entries(counts).map(([name, count]) => ({
      name,
      count,
      percentage: (count / validReqs.length) * 100,
      color: SUBCHARACTERISTIC_COLORS[name] || '#667eea',
      icon: SUBCHARACTERISTIC_ICONS[name] || '📊'
    }));

    // Ordenar por cantidad descendente
    return stats.sort((a, b) => b.count - a.count);
  });

  // Tasa de éxito
  successRate = computed(() => {
    if (!this.results || this.results.total_comments === 0) {
      return 0;
    }
    return (this.results.valid_requirements / this.results.total_comments) * 100;
  });

  // Formatear tiempo
  formatTime(ms: number): string {
    if (ms < 1000) {
      return `${Math.round(ms)}ms`;
    }
    return `${(ms / 1000).toFixed(2)}s`;
  }

  // Formatear score como porcentaje
  formatScore(score: number | null): string {
    if (score === null || score === undefined) {
      return 'N/A';
    }
    return `${(score * 100).toFixed(1)}%`;
  }

  // Obtener clase CSS según el score
  getScoreClass(score: number | null): string {
    if (score === null || score === undefined) {
      return 'score-none';
    }
    if (score >= 0.8) return 'score-high';
    if (score >= 0.6) return 'score-medium';
    return 'score-low';
  }

  // Cambiar tab activo
  setActiveTab(tab: 'table' | 'stats'): void {
    this.activeTab.set(tab);
  }

  // Descargar PDF generado
  downloadPDF(): void {
    if (!this.pdfBlob) {
      return;
    }

    const filename = this.pdfFileName || 'requisitos_usabilidad.pdf';
    this.apiService.downloadPDF(this.pdfBlob, filename);
  }
}
