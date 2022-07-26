package pl.splinter.backend.service;

import lombok.Getter;
import lombok.Setter;
import pl.splinter.backend.entity.Exam;
import pl.splinter.backend.entity.Subject;

@Getter
@Setter
public class ScanData {
    Exam exam;
    Subject subject;
}
