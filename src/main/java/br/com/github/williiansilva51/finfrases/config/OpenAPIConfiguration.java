package br.com.github.williiansilva51.finfrases.config;

import org.springframework.context.annotation.Configuration;
import io.swagger.v3.oas.annotations.OpenAPIDefinition;
import io.swagger.v3.oas.annotations.info.Contact;
import io.swagger.v3.oas.annotations.info.Info;

@Configuration
@OpenAPIDefinition(info = @Info(
        title = "FinFrases API",
        version = "v0.0.1",
        description = "Documentação técnica dos serviços do FinFrases API",
        contact = @Contact(name = "Willian Silva", email = "williansilva@alu.ufc.br")))
public class OpenAPIConfiguration {
}
