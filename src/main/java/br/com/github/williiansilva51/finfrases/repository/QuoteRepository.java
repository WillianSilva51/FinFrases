package br.com.github.williiansilva51.finfrases.repository;

import br.com.github.williiansilva51.finfrases.domain.Quote;
import br.com.github.williiansilva51.finfrases.domain.enums.CategoryQuote;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.mongodb.repository.Aggregation;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface QuoteRepository extends MongoRepository<Quote, String> {

    @Aggregation(pipeline = {
            "{ '$match': { 'verified': true } }",
            "{ '$sample': { 'size': ?0 } }"
    })
    List<Quote> findRandomVerifiedQuotes(int size);

    Page<Quote> findByVerifiedTrue(Pageable pageable);

    Page<Quote> findByAuthorAndVerifiedTrue(String author, Pageable pageable);

    Page<Quote> findByTagsContainingAndVerifiedTrue(CategoryQuote tag, Pageable pageable);
}
