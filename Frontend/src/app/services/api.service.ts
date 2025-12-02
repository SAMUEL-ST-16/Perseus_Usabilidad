import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, forkJoin } from 'rxjs';
import { map } from 'rxjs/operators';
import { SingleCommentRequest, PlayStoreURLRequest, ProcessingResponse } from '../models/requirement.model';
import { environment } from '../../environments/environment';

/**
 * Servicio para conectar con el backend FastAPI
 * Maneja las 3 funcionalidades principales:
 * 1. Procesar comentario único
 * 2. Procesar archivo CSV
 * 3. Procesar URL de Google Play Store
 */
@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private http = inject(HttpClient);

  // URL base del backend desde configuración de ambiente
  private readonly API_URL = environment.apiUrl;

  /**
   * Procesar un comentario único
   * @param comment Texto del comentario
   * @returns Observable con el PDF generado
   */
  processSingleComment(comment: string): Observable<Blob> {
    const request: SingleCommentRequest = { comment };

    return this.http.post(
      `${this.API_URL}/process/single`,
      request,
      {
        responseType: 'blob', // Importante: el backend retorna PDF
        headers: new HttpHeaders({
          'Content-Type': 'application/json'
        })
      }
    );
  }

  /**
   * Procesar archivo CSV con comentarios
   * @param file Archivo CSV
   * @returns Observable con el PDF generado
   */
  processCSVFile(file: File): Observable<Blob> {
    const formData = new FormData();
    formData.append('file', file, file.name);

    return this.http.post(
      `${this.API_URL}/process/csv`,
      formData,
      {
        responseType: 'blob' // Importante: el backend retorna PDF
      }
    );
  }

  /**
   * Procesar URL de Google Play Store
   * @param url URL de la aplicación en Play Store
   * @returns Observable con el PDF generado
   */
  processPlayStoreURL(url: string): Observable<Blob> {
    const request: PlayStoreURLRequest = { url };

    return this.http.post(
      `${this.API_URL}/process/playstore`,
      request,
      {
        responseType: 'blob', // Importante: el backend retorna PDF
        headers: new HttpHeaders({
          'Content-Type': 'application/json'
        })
      }
    );
  }

  /**
   * Verificar el estado del backend
   * @returns Observable con el estado de salud
   */
  checkHealth(): Observable<any> {
    return this.http.get(`${this.API_URL}/health`);
  }

  /**
   * Procesar comentario y obtener JSON + PDF
   * @param comment Texto del comentario
   * @returns Observable con { pdf: Blob, results: ProcessingResponse }
   */
  processSingleCommentWithResults(comment: string): Observable<{ pdf: Blob; results: ProcessingResponse }> {
    const request: SingleCommentRequest = { comment };

    const pdf$ = this.http.post<Blob>(
      `${this.API_URL}/process/single`,
      request,
      {
        responseType: 'blob' as 'json',
        headers: new HttpHeaders({ 'Content-Type': 'application/json' })
      }
    );

    const results$ = this.http.post<ProcessingResponse>(
      `${this.API_URL}/analyze/single`,
      request,
      {
        headers: new HttpHeaders({ 'Content-Type': 'application/json' })
      }
    );

    return forkJoin({ pdf: pdf$, results: results$ });
  }

  /**
   * Procesar CSV y obtener JSON + PDF
   * @param file Archivo CSV
   * @returns Observable con { pdf: Blob, results: ProcessingResponse }
   */
  processCSVWithResults(file: File): Observable<{ pdf: Blob; results: ProcessingResponse }> {
    const formData = new FormData();
    formData.append('file', file, file.name);

    const pdf$ = this.http.post<Blob>(
      `${this.API_URL}/process/csv`,
      formData,
      { responseType: 'blob' as 'json' }
    );

    const results$ = this.http.post<ProcessingResponse>(
      `${this.API_URL}/analyze/csv`,
      formData
    );

    return forkJoin({ pdf: pdf$, results: results$ });
  }

  /**
   * Procesar Play Store y obtener JSON + PDF
   * @param url URL de Play Store
   * @returns Observable con { pdf: Blob, results: ProcessingResponse }
   */
  processPlayStoreWithResults(url: string): Observable<{ pdf: Blob; results: ProcessingResponse }> {
    const request: PlayStoreURLRequest = { url };

    const pdf$ = this.http.post<Blob>(
      `${this.API_URL}/process/playstore`,
      request,
      {
        responseType: 'blob' as 'json',
        headers: new HttpHeaders({ 'Content-Type': 'application/json' })
      }
    );

    const results$ = this.http.post<ProcessingResponse>(
      `${this.API_URL}/analyze/playstore`,
      request,
      {
        headers: new HttpHeaders({ 'Content-Type': 'application/json' })
      }
    );

    return forkJoin({ pdf: pdf$, results: results$ });
  }

  /**
   * Descargar el PDF generado
   * @param blob Blob del PDF
   * @param filename Nombre del archivo
   */
  downloadPDF(blob: Blob, filename: string = 'requisitos_usabilidad.pdf'): void {
    // Crear un enlace temporal para descargar
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    link.click();

    // Limpiar
    window.URL.revokeObjectURL(url);
  }
}
