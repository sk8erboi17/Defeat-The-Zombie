package it.sk8erboi.customproject.world;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.RequiredArgsConstructor;

import java.util.UUID;

@Data
@RequiredArgsConstructor
public class Enemy {
    private final UUID uuid;
    private double x,y;
    private boolean right;
    //TODO Add monster type , attributes ecc.
}
