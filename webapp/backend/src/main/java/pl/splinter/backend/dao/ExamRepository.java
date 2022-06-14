package pl.splinter.backend.dao;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.RequestParam;
import pl.splinter.backend.entity.Exam;

import java.util.List;

@CrossOrigin("http://localhost:4200")
public interface ExamRepository extends JpaRepository<Exam, Long> {
    List<Exam> findByUserUsername(@RequestParam("username")String username);
    List<Exam> findBySubjectIdAndUserUsername(@RequestParam("id")Long id, @RequestParam("username")String username);
}
