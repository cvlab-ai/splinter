import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ExamResultListComponent } from './exam-result-list.component';

describe('ExamResultListComponent', () => {
  let component: ExamResultListComponent;
  let fixture: ComponentFixture<ExamResultListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ExamResultListComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ExamResultListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
