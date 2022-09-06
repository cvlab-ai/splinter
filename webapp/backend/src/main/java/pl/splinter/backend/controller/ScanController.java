package pl.splinter.backend.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import pl.splinter.backend.service.ScanData;
import pl.splinter.backend.service.ScanService;

@CrossOrigin("http://splinter_frontend:4200")
@RestController
@RequestMapping("/api/scan")
public class ScanController {
    private final ScanService scanService;

    @Autowired
    public ScanController(ScanService service) {
        this.scanService = service;
    }

    @PostMapping("/save")
    public void saveScan(@RequestBody ScanData data) {
        scanService.saveScan(data);
    }
}
