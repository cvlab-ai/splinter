import {Injectable} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {map, Observable} from "rxjs";
import {UserService} from "./user.service";
import {Subject} from "../common/subject";

@Injectable({
  providedIn: 'root'
})
export class SubjectService {
  baseUrl = 'http://localhost:8080/api/subjects';
  constructor(private http: HttpClient, private userService: UserService) { }

  getSubjectByUsername(): Observable<Subject[]> {
    const username = this.userService.getUsername();

    const searchUrl = `${this.baseUrl}/search/findByUserUsername?username=${username}`
    return this.http.get<GetResponseSubject>(searchUrl).pipe(map(response => response._embedded.subjects))
  }
}

interface GetResponseSubject {
  _embedded: {
    subjects: Subject[];
  },
  page: {
    size: number;
    totalElements: number;
    totalPages: number;
    number: number;
  }
}
