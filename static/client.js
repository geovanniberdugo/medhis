import { createUploadLink } from 'apollo-upload-client';
import { InMemoryCache } from 'apollo-cache-inmemory';
import { ApolloClient } from 'apollo-client';
import { onError } from 'apollo-link-error';
import { ApolloLink } from 'apollo-link';

if (!window.__APOLLO_CLIENT__) {
    const client = new ApolloClient({
        link: ApolloLink.from([
            onError(({ graphQLErrors, networkError }) => {
                if (graphQLErrors) {
                    graphQLErrors.map(({ message, locations, path }) => {
                        console.log(`[GraphQL error]: Message: ${message}, Location: ${locations}, Path: ${path}`);
                    });
                }
                if (networkError) console.log(`[Network error]: ${networkError}`);
            }),
            createUploadLink({
                uri: '/graphql2/',
                credentials: 'same-origin',
            }),
        ]),
        cache: new InMemoryCache(),
    });

    window.__APOLLO_CLIENT__ = client;
}
