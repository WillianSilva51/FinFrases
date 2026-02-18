package br.com.github.williiansilva51.finfrases.dto.response;

public record FieldErrorResponse(
        String field,
        String message
) {
}
