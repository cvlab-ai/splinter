import {Component, OnInit} from '@angular/core';
import {SubjectService} from "../../../services/subject.service";
import {Subject} from "../../../common/subject";
import {Exam} from "../../../common/exam";
import {ExamService} from "../../../services/exam.service";
import {FormBuilder} from "@angular/forms";
import {ScanService} from "../../../services/scan.service";
import {Router} from "@angular/router";
import {ScanData} from "../../../common/scan-data";

@Component({
  selector: 'app-exam-scan',
  templateUrl: './exam-scan.component.html',
  styleUrls: ['./exam-scan.component.css']
})
export class ExamScanComponent implements OnInit {
  subjects: Subject[] | any;
  exams: Exam[] | any;

  addNewExam = false;
  addNewSubject = false;

  newSubject: Subject = new Subject();
  newExam: Exam = new Exam();

  examFile: string | undefined;

  selectedSubjectId: number | any;
  selectedExamId: number | any;

  constructor(private subjectService: SubjectService, private examService: ExamService, private formBuilder: FormBuilder,
              private scanService: ScanService,  private router: Router) {
  }

  ngOnInit(): void {
    this.subjectService.getSubjectByUsername().subscribe(data => {
      this.subjects = data;
      // Set default exam for html
      this.examService.getExamsBySubjectId(this.subjects[0].id).subscribe(res => this.exams = res);
    })
  }

  subjectChosen(subjectId: number) {
    this.examService.getExamsBySubjectId(subjectId).subscribe(data => this.exams = data);
    this.selectedSubjectId = subjectId;
  }

  examChosen(examId: number) {
    this.selectedExamId = examId;
  }

  addExam() {
    this.addNewExam = true;
  }

  hideAddExam() {
    this.addNewExam = false;
  }

  addSubject() {
    this.addNewSubject = true;
  }

  hideAddSubject() {
    this.addNewSubject = false;
  }

  setExamName(value: string) {
    this.newExam.name = value;
  }

  setExamDesc(value: string) {
    this.newExam.description = value;
  }

  setSubjectName(value: string) {
    this.newSubject.name = value;
  }

  setSubjectDsc(value: string) {
    this.newSubject.description = value;
  }

  setFile(data: any) {
    const reader = new FileReader();
    reader.readAsDataURL(data.target.files.item(0));
    reader.onload = (event) => {
      // @ts-ignore
      this.newExam.file = event.target.result.split('data:application/pdf;base64,')[1];
      // @ts-ignore
      this.examFile = event.target.result.split('data:application/pdf;base64,')[1];
    };
  }

  onSubmit() {
    // TODO validation
    let scanData = new ScanData();
    if (this.addNewExam) {
      scanData.exam = this.newExam;
    } else {
      scanData.exam = new Exam();
      scanData.exam.id = this.selectedExamId;
      scanData.exam.file = this.examFile;
    }

    if (this.addNewSubject) {
      scanData.subject = this.newSubject;
    } else {
      scanData.subject = new Subject();
      scanData.subject.id = this.selectedSubjectId;
    }

    console.log("X")

    this.scanService.save(scanData).subscribe({
      next: response => {
        setTimeout(() => {
          alert("Dodano!");
          this.router.navigateByUrl("/");
          window.location.reload();
        }, 2000);
      }, error: err => {
        alert(`Wystąpił bład zapisu: ${JSON.stringify(err)}`);
      }
    })
  }
}
