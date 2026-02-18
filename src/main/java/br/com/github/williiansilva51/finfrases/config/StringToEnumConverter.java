package br.com.github.williiansilva51.finfrases.config;

import br.com.github.williiansilva51.finfrases.domain.enums.CategoryQuote;
import lombok.extern.slf4j.Slf4j;
import org.springframework.core.convert.converter.Converter;
import org.springframework.stereotype.Component;

@Component
@Slf4j
public class StringToEnumConverter implements Converter<String, CategoryQuote> {
    @Override
    public CategoryQuote convert(String source) {
        try {
            return CategoryQuote.valueOf(source.toUpperCase());
        } catch (IllegalArgumentException e) {
            log.error("Category not found: {}", source);
            return null;
        }
    }
}