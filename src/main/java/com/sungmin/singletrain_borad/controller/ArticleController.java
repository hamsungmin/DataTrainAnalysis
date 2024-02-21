package com.sungmin.singletrain_borad.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;

@RequestMapping("/articles")
@Controller
public class ArticleController {
    @GetMapping
    public String articles(){

        return "articles/index";
    }
}
