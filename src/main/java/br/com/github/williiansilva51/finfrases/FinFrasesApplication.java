package br.com.github.williiansilva51.finfrases;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cache.annotation.EnableCaching;

@SpringBootApplication
public class FinFrasesApplication {

    public static void main(String[] args) {
        SpringApplication.run(FinFrasesApplication.class, args);
    }

}
