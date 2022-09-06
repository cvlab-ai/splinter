package pl.splinter.backend.dao;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.RequestParam;
import pl.splinter.backend.entity.ExamResult;

import java.util.List;

@CrossOrigin("http://splinter_frontend:4200")
public interface ExamResultRepository extends JpaRepository<ExamResult, Long> {
    List<ExamResult> findByExamId(@RequestParam("id")Long id);
}
