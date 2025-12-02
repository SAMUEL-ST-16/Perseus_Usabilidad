import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { ISO25010_SECURITY_SUBCHARACTERISTICS, ISO25010_OVERVIEW } from '../../data/iso25010.data';

/**
 * Componente ISO25010 - Página informativa
 * Muestra información completa sobre ISO/IEC 25010:2023 y las
 * 8 subcaracterísticas de usabilidad
 */
@Component({
  selector: 'app-iso25010',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './iso25010.html',
  styleUrl: './iso25010.css'
})
export class ISO25010Component {
  overview = ISO25010_OVERVIEW;
  subcharacteristics = ISO25010_SECURITY_SUBCHARACTERISTICS;

  // Para mostrar/ocultar detalles de cada subcaracterística
  expandedIndex: number | null = null;

  toggleDetails(index: number): void {
    this.expandedIndex = this.expandedIndex === index ? null : index;
  }

  isExpanded(index: number): boolean {
    return this.expandedIndex === index;
  }
}
