package br.com.github.williiansilva51.finfrases.controller;

import br.com.github.williiansilva51.finfrases.domain.enums.CategoryQuote;
import br.com.github.williiansilva51.finfrases.dto.request.CreateQuoteRequest;
import br.com.github.williiansilva51.finfrases.dto.response.PaginatedResponse;
import br.com.github.williiansilva51.finfrases.dto.response.QuoteResponse;
import br.com.github.williiansilva51.finfrases.service.QuoteService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import jakarta.validation.Valid;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Pageable;
import org.springframework.data.web.PageableDefault;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import java.net.URI;
import java.util.List;

@RestController
@RequestMapping(value = "v1/quotes")
@RequiredArgsConstructor
@Validated
public class QuoteController {
    private final QuoteService quoteService;

    @PostMapping
    @Operation(summary = "Cria uma frase", description = "Cria uma frase com os dados informados")
    @ApiResponse(responseCode = "200", description = "Frase criada com sucesso")
    public ResponseEntity<QuoteResponse> createQuote(@Valid @RequestBody CreateQuoteRequest quoteRequest) {
        QuoteResponse quoteResponse = quoteService.createQuote(quoteRequest);

        return ResponseEntity.created(URI.create("/quotes/random")).body(quoteResponse);
    }

    @GetMapping("/random")
    @Operation(summary = "Retorna um frase aleatória")
    @ApiResponse(responseCode = "200", description = "Frase retornada com sucesso")
    public ResponseEntity<List<QuoteResponse>> getRandomQuote(@Min(value = 1, message = "O valor mínimo é 1")
                                                                  @Max(value = 50, message = "O valor máximo é 50")
                                                                  @RequestParam(defaultValue = "1") int size) {
        return ResponseEntity.ok(quoteService.getRandomQuotes(size));
    }

    @GetMapping
    @Operation(summary = "Retorna todas as frases", description = "Retorna todas as frases ordenadas pelo autor")
    @ApiResponse(responseCode = "200", description = "Lista de frases retornada com sucesso")
    public ResponseEntity<PaginatedResponse<QuoteResponse>> getAllQuotes(@PageableDefault(sort = "author") Pageable pageable)
    {
        return ResponseEntity.ok(quoteService.getAllQuotes(pageable));
    }

    @GetMapping("/author/{author}")
    @Operation(summary = "Retorna todas as frases de um autor", description = "Retorna todas as frases de um autor ordenadas pelo autor")
    @ApiResponse(responseCode = "200", description = "Lista de frases retornada com sucesso")
    public ResponseEntity<PaginatedResponse<QuoteResponse>> getQuotesByAuthor(@PathVariable String author, @PageableDefault(sort = "content") Pageable pageable)
    {
        return ResponseEntity.ok(quoteService.getQuotesByAuthor(author, pageable));
    }

    @GetMapping("/tag/{tag}")
    @Operation(summary = "Retorna todas as frases de uma tag", description = "Retorna todas as frases de uma tag ordenadas pelo autor")
    @ApiResponse(responseCode = "200", description = "Lista de frases retornada com sucesso")
    public ResponseEntity<PaginatedResponse<QuoteResponse>> getQuotesByTag(@PathVariable CategoryQuote tag, @PageableDefault(sort = "content") Pageable pageable) {
        return ResponseEntity.ok(quoteService.getQuotesByTagsContainingAndVerifiedTrue(tag,pageable));
    }
}
