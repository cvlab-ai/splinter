import { Component, OnInit } from '@angular/core';
import {ExamService} from "../../../services/exam.service";
import {ExamResult} from "../../../common/exam-result";
import {ActivatedRoute} from "@angular/router";

@Component({
  selector: 'app-exam-result-list',
  templateUrl: './exam-result-list.component.html',
  styleUrls: ['./exam-result-list.component.css']
})
export class ExamResultListComponent implements OnInit {
  examResults: ExamResult[] | any;
  examName: string | any;
  constructor(private examService: ExamService, private route: ActivatedRoute) { }

  ngOnInit(): void {
    // @ts-ignore
    const examId = +this.route.snapshot.paramMap.get('id');
    this.examService.getResultByExamId(examId).subscribe(data => {
      this.examResults = data;
      this.examName = data[0].name;
    });
  }

}
