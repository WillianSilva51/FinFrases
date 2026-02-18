package br.com.github.williiansilva51.finfrases.exception;

import br.com.github.williiansilva51.finfrases.dto.response.ErrorResponse;
import br.com.github.williiansilva51.finfrases.dto.response.FieldErrorResponse;
import jakarta.servlet.http.HttpServletRequest;
import lombok.extern.slf4j.Slf4j;
import org.jspecify.annotations.NonNull;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.HttpRequestMethodNotSupportedException;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.web.method.annotation.MethodArgumentTypeMismatchException;

import java.time.Instant;
import java.util.List;

@RestControllerAdvice
@Slf4j
public class GlobalExceptionHandler {
    private @NonNull ResponseEntity<ErrorResponse> generateErrorResponse(HttpStatus httpStatus, String ex,
                                                                         List<FieldErrorResponse> fieldErrorResponse,
                                                                         HttpServletRequest request) {
        ErrorResponse response = new ErrorResponse(
                httpStatus.value(),
                httpStatus.getReasonPhrase(),
                ex,
                request.getRequestURI(),
                Instant.now(),
                fieldErrorResponse
        );

        return ResponseEntity.status(httpStatus).body(response);
    }

    private @NonNull ResponseEntity<ErrorResponse> generateErrorResponse(HttpStatus httpStatus, String ex, HttpServletRequest request) {
        return generateErrorResponse(httpStatus, ex, null, request);
    }

    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleNotFound(ResourceNotFoundException ex, HttpServletRequest request) {
        return generateErrorResponse(HttpStatus.NOT_FOUND, ex.getMessage(), request);
    }


    @ExceptionHandler(DomainValidationException.class)
    public ResponseEntity<ErrorResponse> handleBadRequest(DomainValidationException ex, HttpServletRequest request) {
        return generateErrorResponse(HttpStatus.BAD_REQUEST, ex.getMessage(), request);
    }

    @ExceptionHandler(IllegalArgumentException.class)
    public ResponseEntity<ErrorResponse> handleBadRequest(IllegalArgumentException ex, HttpServletRequest request) {
        return generateErrorResponse(HttpStatus.BAD_REQUEST, ex.getMessage(), request);
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleBadRequest(MethodArgumentNotValidException ex, HttpServletRequest request) {
        List<FieldErrorResponse> responseList = ex.getFieldErrors()
                .stream()
                .map(error -> new FieldErrorResponse(
                        error.getField(),
                        error.getDefaultMessage()))
                .toList();

        return generateErrorResponse(HttpStatus.BAD_REQUEST, "Validation Error", responseList, request);
    }

    @ExceptionHandler(HttpRequestMethodNotSupportedException.class)
    public ResponseEntity<ErrorResponse> handleMethodNotSupported(HttpRequestMethodNotSupportedException ex, HttpServletRequest request) {
        return generateErrorResponse(HttpStatus.METHOD_NOT_ALLOWED, ex.getMessage(), request);
    }

    @ExceptionHandler(MethodArgumentTypeMismatchException.class)
    public ResponseEntity<ErrorResponse> handleBadRequest(MethodArgumentTypeMismatchException ex, HttpServletRequest request) {
        return generateErrorResponse(HttpStatus.BAD_REQUEST, ex.getMessage(), request);
    }

    @ExceptionHandler(DataIntegrityViolationException.class)
    public ResponseEntity<ErrorResponse> handleBadRequest(DataIntegrityViolationException ex, HttpServletRequest request) {
        return generateErrorResponse(HttpStatus.BAD_REQUEST, ex.getMessage(), request);
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleInternalServerError(Exception ex, HttpServletRequest request) {
        log.error(
                "Erro interno inesperado. Path: {}, Method: {}, Message: {}",
                request.getRequestURI(),
                request.getMethod(),
                ex.getMessage(),
                ex
        );

        return generateErrorResponse(HttpStatus.INTERNAL_SERVER_ERROR, "Ocorreu um erro interno inesperado.", request);
    }
}
