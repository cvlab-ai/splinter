import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {UserService} from "./user.service";
import {map, Observable} from "rxjs";
import {Exam} from "../common/exam";
import {ExamResult} from "../common/exam-result";

@Injectable({
  providedIn: 'root'
})
export class ExamService {
  baseUrl = 'http://localhost:8080/api/exams';
  resultUrl = 'http://localhost:8080/api/examResults';

  constructor(private http: HttpClient, private userService: UserService) { }

  getExamsByUsername(): Observable<Exam[]> {
    const username = this.userService.getUsername();

    const searchUrl = `${this.baseUrl}/search/findByUserUsername?username=${username}`
    return this.http.get<GetResponseExam>(searchUrl).pipe(map(response => response._embedded.exams))
  }

  getExamsBySubjectId(subjectId: number | any): Observable<Exam[]> {
    const username = this.userService.getUsername();
    const searchUrl = `${this.baseUrl}/search/findBySubjectIdAndUserUsername?id=${subjectId}&username=${username}`;
    return this.http.get<GetResponseExam>(searchUrl).pipe(map(response => response._embedded.exams))
  }

  getResultByExamId(examId: number | any): Observable<ExamResult[]> {
    const searchUrl = `${this.resultUrl}/search/findByExamId?id=${examId}`
    return this.http.get<GetResponseExamResult>(searchUrl).pipe(map(response => response._embedded.examResults))
  }
}

interface GetResponseExam {
  _embedded: {
    exams: Exam[];
  },
  page: {
    size: number;
    totalElements: number;
    totalPages: number;
    number: number;
  }
}
interface GetResponseExamResult {
  _embedded: {
    examResults: ExamResult[];
  }
}
