package br.com.github.williiansilva51.finfrases.domain;

import br.com.github.williiansilva51.finfrases.domain.enums.CategoryQuote;
import lombok.*;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.index.Indexed;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

import java.time.LocalDateTime;
import java.util.List;

@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Document(collection = "quotes")
public class Quote {
    @Id
    private String id;

    @Field("content")
    private String content;

    @Field("author")
    @Indexed
    private String author;

    @Field("category")
    @Indexed
    private List<CategoryQuote> tags;

    @Field("source")
    private String source;

    @Field("verified")
    private boolean verified;

    @Builder.Default
    private LocalDateTime createdAt = LocalDateTime.now();
}
