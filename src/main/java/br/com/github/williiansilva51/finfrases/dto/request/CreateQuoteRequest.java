package br.com.github.williiansilva51.finfrases.dto.request;

import br.com.github.williiansilva51.finfrases.domain.enums.CategoryQuote;
import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

import java.util.List;

public record CreateQuoteRequest(
        @Schema(description = "Conteúdo da frase", example = "O risco vem de não saber o que você está fazendo.")
        @NotBlank(message = "O conteúdo da frase não pode ser vazio")
        @Size(max = 500, message = "A frase deve ter no máximo 500 caracteres")
        String content,

        @Schema(description = "Autor da frase", example = "Warren Buffett")
        @NotBlank(message = "A frase deve ter um autor")
        @Size(max = 100, message = "O autor da frase deve ter no máximo 100 caracteres")
        String author,

        @Schema(description = "Categorias da frase", example = "[\"INVESTIMENTOS\", \"PSICOLOGIA\"]")
        @NotEmpty(message = "A frase deve ter pelo menos uma categoria")
        List<CategoryQuote> tags,

        @Schema(description = "Fonte da frase", example = "Livro: O Investidor Inteligente")
        String source
) {
}
