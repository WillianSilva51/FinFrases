package br.com.github.williiansilva51.finfrases.service;

import br.com.github.williiansilva51.finfrases.domain.Quote;
import br.com.github.williiansilva51.finfrases.domain.enums.CategoryQuote;
import br.com.github.williiansilva51.finfrases.dto.request.CreateQuoteRequest;
import br.com.github.williiansilva51.finfrases.dto.response.PaginatedResponse;
import br.com.github.williiansilva51.finfrases.dto.response.QuoteResponse;
import br.com.github.williiansilva51.finfrases.mapper.QuoteMapper;
import br.com.github.williiansilva51.finfrases.repository.QuoteRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@RequiredArgsConstructor
@Transactional
@Service
public class QuoteService {
    private final QuoteMapper quoteMapper;
    private final QuoteRepository quoteRepository;

    private PaginatedResponse<QuoteResponse> toPaginatedResponse(Page<Quote> quotePages) {
        List<QuoteResponse> quotes = quoteMapper.toResponseList(quotePages.getContent());

        return new PaginatedResponse<>(
                quotes,
                quotePages.getTotalElements(),
                quotePages.getTotalPages(),
                quotePages.getNumber()
        );
    }

    public QuoteResponse createQuote(CreateQuoteRequest quoteRequest) {
        Quote quote = quoteMapper.toDomain(quoteRequest);

        Quote savedQuote = quoteRepository.save(quote);

        return quoteMapper.toResponse(savedQuote);
    }

    @Transactional(readOnly = true)
    public List<QuoteResponse> getRandomQuotes(int size) {
        return quoteMapper.toResponseList(quoteRepository.findRandomVerifiedQuotes(size));
    }

    @Transactional(readOnly = true)
    public PaginatedResponse<QuoteResponse> getAllQuotes(Pageable pageable) {
        return toPaginatedResponse(quoteRepository.findByVerifiedTrue(pageable));
    }

    @Transactional(readOnly = true)
    public PaginatedResponse<QuoteResponse> getQuotesByAuthor(String author, Pageable pageable) {
        return toPaginatedResponse(quoteRepository.findByAuthorAndVerifiedTrue(author, pageable));
    }

    @Transactional(readOnly = true)
    public PaginatedResponse<QuoteResponse> getQuotesByTagsContainingAndVerifiedTrue(CategoryQuote tag, Pageable pageable) {
        return toPaginatedResponse(quoteRepository.findByTagsContainingAndVerifiedTrue(tag, pageable));
    }
}
