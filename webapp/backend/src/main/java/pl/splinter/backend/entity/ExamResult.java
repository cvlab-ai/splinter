package pl.splinter.backend.entity;

import lombok.Getter;
import lombok.Setter;

import javax.persistence.*;

@Entity
@Table(name = "EXAM_RESULT")
@Getter
@Setter
public class ExamResult {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id", nullable = false)
    private Long id;

    @Column(name = "name")
    private String name;

    @Column(name = "max_score")
    private String maxScore;

    @Column(name = "score")
    private String score;

    @Column(name = "student")
    private String student;

    @ManyToOne
    @JoinColumn(name = "exam_id")
    private Exam exam;
}
