package it.sk8erboi.customproject;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication
@EnableScheduling
public class CustomProjectApplication {

	public static void main(String[] args) {
		SpringApplication.run(CustomProjectApplication.class, args);
	}

}
