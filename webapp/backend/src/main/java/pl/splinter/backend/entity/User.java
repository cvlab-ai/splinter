package pl.splinter.backend.entity;

import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.Getter;
import lombok.Setter;

import javax.persistence.*;
import java.util.HashSet;
import java.util.Set;

@Entity
@Table(name = "users")
@Getter
@Setter
public class User {
    @Id
    @Column(name = "username")
    private String username;

    @Column(name = "password")
    private String password;

    @Column(name = "email")
    private String email;

    @JsonIgnore
    @OneToMany(mappedBy = "user", cascade = CascadeType.ALL, orphanRemoval = true)
    private Set<Subject> subjects;

    @JsonIgnore
    @OneToMany(mappedBy = "user", cascade = CascadeType.ALL, orphanRemoval = true)
    private Set<Exam> exams;

    public void addSubject(Subject subject) {
        if (subject != null) {
            if (subjects == null) {
                subjects = new HashSet<>();
            }
            subjects.add(subject);
            subject.setUser(this);
        }
    }

    public void addExam(Exam exam) {
        if (exam != null) {
            if (exams == null) {
                exams = new HashSet<>();
            }
            exams.add(exam);
            exam.setUser(this);
        }
    }
}
