package pl.splinter.backend.dao;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.RequestParam;
import pl.splinter.backend.entity.Subject;

import java.util.List;

@CrossOrigin("http://splinter_frontend:4200")
public interface SubjectRepository extends JpaRepository<Subject, Long> {
    List<Subject> findByUserUsername(@RequestParam("username")String username);
}
