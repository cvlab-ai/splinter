import {NgModule} from '@angular/core';
import {BrowserModule} from '@angular/platform-browser';

import {AppComponent} from './app.component';
import {LoginComponent} from './components/login/login.component';
import {NavBarComponent} from './components/nav-bar/nav-bar.component';
import {RegisterComponent} from './components/register/register.component';
import {SubjectListComponent} from './components/subject-list/subject-list.component';
import {ExamResultListComponent} from './components/exam/exam-result-list/exam-result-list.component';
import {ExamListComponent} from './components/exam/exam-list/exam-list.component';
import {ExamScanComponent} from './components/exam/exam-scan/exam-scan.component';
import {RouterModule, Routes} from "@angular/router";
import {HttpClientModule} from "@angular/common/http";
import {FormsModule, ReactiveFormsModule} from "@angular/forms";

const routes: Routes = [
  {path: 'login', component: LoginComponent},
  {path: 'register', component: RegisterComponent},
  {path: 'subjects', component: SubjectListComponent},
  {path: 'exam/:id', component: ExamResultListComponent},
  {path: 'exams/:id', component: ExamListComponent},
  {path: 'exams', component: ExamListComponent},
  {path: 'scan', component: ExamScanComponent},
  {path: '', redirectTo: '/login', pathMatch: 'full'}
];

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    NavBarComponent,
    RegisterComponent,
    SubjectListComponent,
    ExamResultListComponent,
    ExamListComponent,
    ExamScanComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpClientModule,
    RouterModule.forRoot(routes),
    ReactiveFormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {
}
