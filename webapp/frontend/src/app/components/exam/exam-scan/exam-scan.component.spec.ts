import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ExamScanComponent } from './exam-scan.component';

describe('ExamScanComponent', () => {
  let component: ExamScanComponent;
  let fixture: ComponentFixture<ExamScanComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ExamScanComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ExamScanComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
