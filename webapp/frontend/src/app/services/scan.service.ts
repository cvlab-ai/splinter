import {Injectable} from '@angular/core';
import {Exam} from "../common/exam";
import {Observable} from "rxjs";
import {HttpClient} from "@angular/common/http";
import {ScanData} from "../common/scan-data";

@Injectable({
  providedIn: 'root'
})
export class ScanService {
  saveUrl = 'http://localhost:8080/api/scan/save';

  constructor(private http: HttpClient) { }

  save(data: ScanData): Observable<any> {
    return this.http.post<Exam>(this.saveUrl,data);
  }
}
