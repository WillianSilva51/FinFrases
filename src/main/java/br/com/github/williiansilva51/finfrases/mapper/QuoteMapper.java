package br.com.github.williiansilva51.finfrases.mapper;

import br.com.github.williiansilva51.finfrases.domain.Quote;
import br.com.github.williiansilva51.finfrases.dto.request.CreateQuoteRequest;
import br.com.github.williiansilva51.finfrases.dto.response.QuoteResponse;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;

import java.util.List;

@Mapper(componentModel = "spring")
public interface QuoteMapper {
    QuoteResponse toResponse(Quote domain);

    @Mapping(target = "id", ignore = true)
    @Mapping(target = "createdAt", ignore = true)
    @Mapping(target = "verified", constant = "false")
    Quote toDomain(CreateQuoteRequest request);

    List<QuoteResponse> toResponseList(List<Quote> domainList);
}
