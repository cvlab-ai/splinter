package pl.splinter.backend.config;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.rest.core.config.RepositoryRestConfiguration;
import org.springframework.data.rest.webmvc.config.RepositoryRestConfigurer;
import org.springframework.http.HttpMethod;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import pl.splinter.backend.entity.Exam;
import pl.splinter.backend.entity.ExamResult;
import pl.splinter.backend.entity.Subject;

import javax.persistence.EntityManager;
import javax.persistence.metamodel.EntityType;
import java.util.ArrayList;
import java.util.List;
import java.util.Set;


@Configuration
public class MyDataRestConfig implements RepositoryRestConfigurer {
    private EntityManager entityManager;

    @Autowired
    public MyDataRestConfig(EntityManager entityManager)
    {
        this.entityManager = entityManager;
    }

    @Override
    public void configureRepositoryRestConfiguration(RepositoryRestConfiguration config, CorsRegistry cors) {
        HttpMethod[] theUnsupportedMethods = {HttpMethod.PUT, HttpMethod.POST, HttpMethod.DELETE};

        //disable HTTP methods for Product
        disableHttpMethods(Exam.class, config, theUnsupportedMethods);
        disableHttpMethods(ExamResult.class, config, theUnsupportedMethods);
        disableHttpMethods(Subject.class, config, theUnsupportedMethods);

        exposeIds(config);
    }

    private void disableHttpMethods(Class theClass, RepositoryRestConfiguration config, HttpMethod[] theUnsupportedMethods)
    {
        config.getExposureConfiguration()
                .forDomainType(theClass)
                .withItemExposure((metdata, httpMethods) -> httpMethods.disable(theUnsupportedMethods))
                .withCollectionExposure((metdata, httpMethods) -> httpMethods.disable(theUnsupportedMethods));
    }


    private void exposeIds(RepositoryRestConfiguration config)
    {
        Set<EntityType<?>> entityTypeSet = entityManager.getMetamodel().getEntities();

        List<Class> entityClasses = new ArrayList<>();

        entityTypeSet.forEach(entityType -> entityClasses.add(entityType.getJavaType()));

        Class[] domainType = entityClasses.toArray(new Class[0]);
        config.exposeIdsFor(domainType);
    }
}

