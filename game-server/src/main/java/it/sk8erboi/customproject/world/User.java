package it.sk8erboi.customproject.world;

import it.sk8erboi.customproject.api.network.pipeline.out.PipelineOut;
import it.sk8erboi.customproject.api.network.pipeline.out.PipelineOutBuilder;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.Getter;
import lombok.Setter;
import org.apache.catalina.Pipeline;

import java.nio.channels.AsynchronousSocketChannel;

@Data
@Setter
@AllArgsConstructor
public class User {
    private final AsynchronousSocketChannel asynchronousSocketChannel;
    private final String username;
    private double x_coordinate;
    private double y_coordinate;
    private int kill;
}
