import { Component, OnInit } from '@angular/core';
import {SubjectService} from "../../services/subject.service";
import {Subject} from "../../common/subject";
import {ExamService} from "../../services/exam.service";

@Component({
  selector: 'app-subject-list',
  templateUrl: './subject-list.component.html',
  styleUrls: ['./subject-list.component.css']
})
export class SubjectListComponent implements OnInit {
  subjects: Subject[] | any;

  constructor(private subjectService: SubjectService, private examService: ExamService) { }

  ngOnInit(): void {
    this.subjectService.getSubjectByUsername().subscribe(data => {
      this.subjects = data;
      this.subjects.forEach(
        (subject: Subject) => this.examService.getExamsBySubjectId(subject.id)
                              .subscribe( res => subject.examNumber = res.length));
    });
  }

}
