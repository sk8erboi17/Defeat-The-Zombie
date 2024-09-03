package it.sk8erboi.customproject.controller;

import it.sk8erboi.customproject.services.EnemyService;
import it.sk8erboi.customproject.services.NetworkService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping(value = "game/v1/api/")
@CrossOrigin(origins = "http://localhost")
public class StatsController {

    @Autowired
    private NetworkService networkService;

    @Autowired
    private EnemyService enemyService;

    @GetMapping("online")
    //updates the onlines player
    public ResponseEntity<Integer> online() {
        return ResponseEntity.ok().body(networkService.getUserList().size());
    }

    @GetMapping("entities")
    //updates the entities
    public ResponseEntity<Integer> entity() {
        return ResponseEntity.ok().body(enemyService.getEnemies().size());
    }
}
