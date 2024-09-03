package it.sk8erboi.customproject.world.ai;

import it.sk8erboi.customproject.world.Enemy;

public class EnemyAI {

    //logic movement for the enemy
    public static void moveX(Enemy enemy){
        if(enemy.isRight()){
            enemy.setX(enemy.getX() - 0.5);
        }else{
            enemy.setX(enemy.getX() + 0.5);
        }

    }
}
