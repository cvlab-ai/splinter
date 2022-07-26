package pl.splinter.backend.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import pl.splinter.backend.dao.ExamRepository;
import pl.splinter.backend.dao.SubjectRepository;
import pl.splinter.backend.entity.Exam;
import pl.splinter.backend.entity.Subject;

@Service
public class ScanServiceImpl implements ScanService{
    @Autowired
    private ExamRepository examRepository;

    @Autowired
    private SubjectRepository subjectRepository;

    @Override
    public void saveScan(ScanData data) {
        Subject subject = data.getSubject();
        Exam exam = data.getExam();
        // TODO when dont have id, when have id
        if (exam.getId() != null) {
            String file = exam.getFile();

            exam = this.examRepository.findById(exam.getId()).get();
            exam.setFile(file);
        }

        if (subject.getId() != null) {
            subject = subjectRepository.findById(subject.getId()).get();
        }

        subject.addExam(exam);

        subjectRepository.save(subject);
    }
}
