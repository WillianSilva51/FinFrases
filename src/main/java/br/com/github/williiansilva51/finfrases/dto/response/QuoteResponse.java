package br.com.github.williiansilva51.finfrases.dto.response;

import br.com.github.williiansilva51.finfrases.domain.enums.CategoryQuote;
import io.swagger.v3.oas.annotations.media.Schema;
import java.util.List;

public record QuoteResponse(

        @Schema(description = "Identificador único da frase", example = "65d4f8a9e4b0a1b2c3d4e5f6")
        String id,

        @Schema(description = "O texto da frase", example = "O preço é o que você paga; o valor é o que você leva.")
        String content,

        @Schema(description = "Autor", example = "Warren Buffett")
        String author,

        @Schema(description = "Categorias relacionadas")
        List<CategoryQuote> tags,

        @Schema(description = "Fonte da informação (Livro/Url)", example = "Carta aos Acionistas, 2008")
        String source
) {
}