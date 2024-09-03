package it.sk8erboi.customproject.services;

import it.sk8erboi.customproject.world.Enemy;
import lombok.Getter;
import org.springframework.stereotype.Service;

import java.util.UUID;
import java.util.concurrent.CopyOnWriteArrayList;

@Getter
@Service
public class EnemyService {
    private final CopyOnWriteArrayList<Enemy> enemies = new CopyOnWriteArrayList<>();

    public void add(Enemy enemy) {
        enemies.add(enemy);
    }

    public void remove(Enemy enemy){
        enemies.remove(enemy);
    }

    public Enemy getEnemyByUuid(UUID uuid) {
        return enemies.stream().filter(enemy ->  enemy.getUuid().equals(uuid)).findAny().orElseThrow(() -> new NullPointerException("Enemy not found"));
    }

}
