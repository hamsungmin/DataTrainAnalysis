package com.sungmin.singletrain_borad.controller;

import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@WebMvcTest(ArticleController.class)
@Controller
public class ArticleControllerTest {
    @GetMapping
    public String articles(){

        return "articles/index";
    }

}
