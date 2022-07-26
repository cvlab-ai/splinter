import { Component, OnInit } from '@angular/core';
import {ExamService} from "../../../services/exam.service";
import {Exam} from "../../../common/exam";
import {ActivatedRoute} from "@angular/router";

@Component({
  selector: 'app-exam-list',
  templateUrl: './exam-list.component.html',
  styleUrls: ['./exam-list.component.css']
})
export class ExamListComponent implements OnInit {
  exams: Exam[] | undefined;
  constructor(private examService: ExamService, private route: ActivatedRoute) { }

  ngOnInit(): void {
    this.route.paramMap.subscribe(() => {
      const hasId = this.route.snapshot.paramMap.has('id');
      if (hasId) {
        // @ts-ignore
        const subjectId = +this.route.snapshot.paramMap.get('id');
        this.examService.getExamsBySubjectId(subjectId).subscribe(data => {
          this.exams = data;
          // Get number of exam results
          this.exams.forEach(exam => this.examService.getResultByExamId(exam.id).subscribe(result => exam.resultNumber = result.length))
        });
      } else {
        this.listExamsByUsername();
      }
    });
  }

  private listExamsByUsername() {
    this.examService.getExamsByUsername().subscribe(data => {
      this.exams = data;
      this.exams.forEach(exam => this.examService.getResultByExamId(exam.id).subscribe(result => exam.resultNumber = result.length))
    });
  }
}
