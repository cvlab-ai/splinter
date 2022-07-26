package pl.splinter.backend.entity;

import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.Getter;
import lombok.Setter;

import javax.persistence.*;
import java.util.HashSet;
import java.util.Set;

@Entity
@Table(name = "SUBJECT")
@Getter
@Setter
public class Subject {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id", nullable = false)
    private Long id;

    @Column(name = "name")
    private String name;

    @Column(name = "description")
    private String description;

    @JsonIgnore
    @OneToMany(mappedBy = "subject", cascade = CascadeType.ALL, orphanRemoval = true)
    private Set<Exam> exams;

    @ManyToOne
    @JoinColumn(name = "user_id")
    private User user;

    public void addExam(Exam exam) {
        if (exam != null) {
            if (exams == null) {
                exams = new HashSet<>();
            }

            exams.add(exam);
            exam.setSubject(this);
        }
    }
}
