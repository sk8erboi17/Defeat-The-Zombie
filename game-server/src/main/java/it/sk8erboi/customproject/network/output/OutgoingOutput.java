package it.sk8erboi.customproject.network.output;

import it.sk8erboi.customproject.api.network.pipeline.out.PipelineOut;
import it.sk8erboi.customproject.api.network.pipeline.out.PipelineOutBuilder;
import it.sk8erboi.customproject.services.EnemyService;
import it.sk8erboi.customproject.world.Enemy;
import it.sk8erboi.customproject.world.User;
import it.sk8erboi.customproject.services.NetworkService;
import it.sk8erboi.customproject.world.ai.EnemyAI;
import jakarta.annotation.PostConstruct;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.Random;
import java.util.UUID;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

@Component
public class OutgoingOutput {

    @Autowired
    private EnemyService enemyService;

    @Autowired
    private NetworkService networkService;

    private final ScheduledExecutorService scheduledExecutorService = Executors.newScheduledThreadPool(8);

    @PostConstruct
    public void init() {
        Random random = new Random();
        scheduledExecutorService.scheduleWithFixedDelay(() -> {

            //check if there are users
            if (networkService.getUserList().isEmpty()) return;

            //limit spawn mob to 4
            if(enemyService.getEnemies().size() > 4) return;

            //create the enemy and send enemy to the client
            UUID mobUuid = UUID.randomUUID();
            boolean isRight = random.nextBoolean();
            Enemy enemy = new Enemy(mobUuid);
            enemyService.add(enemy);
            enemy.setRight(isRight);
            for (User user : networkService.getUserList()) {
                //create a output channel from the server to the client
                PipelineOut pipelineOut = new PipelineOutBuilder(user.getAsynchronousSocketChannel())
                        .allocateDirect(true).setBufferSize(4096).buildSocket();

                //handle the outputs
                if (isRight) {
                    pipelineOut.handleRequest(new StringServerOut("spawn_enemy:" + mobUuid + ":750:463"));
                    enemy.setX(750);
                    enemy.setY(463);
                } else {
                    pipelineOut.handleRequest(new StringServerOut("spawn_enemy:" + mobUuid + ":12:463"));
                    enemy.setX(12);
                    enemy.setY(463);
                }
            }
        }, 300, 3000, TimeUnit.MILLISECONDS);

        scheduledExecutorService.scheduleAtFixedRate(() ->{
            enemyService.getEnemies().parallelStream().forEach((enemies) ->{
                for (User user : networkService.getUserList()) {
                    EnemyAI.moveX(enemies);
                    //send packets to the client
                    PipelineOut pipelineOut = new PipelineOutBuilder(user.getAsynchronousSocketChannel()).allocateDirect(true).setBufferSize(8196).buildSocket();
                    pipelineOut.handleRequest(new StringServerOut("move_enemy:" + enemies.getUuid() + ":" + enemies.getX() + ":" + enemies.getY() + ":" + enemies.isRight()));
                }
            });
    },200,100,TimeUnit.MILLISECONDS);
    }

}
