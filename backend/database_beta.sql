-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema match_score_project
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema match_score_project
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `match_score_project` DEFAULT CHARACTER SET latin1 ;
USE `match_score_project` ;

-- -----------------------------------------------------
-- Table `match_score_project`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `match_score_project`.`users` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(45) NOT NULL,
  `password` VARCHAR(99) NOT NULL,
  `user_type` VARCHAR(45) NOT NULL DEFAULT 'user',
  PRIMARY KEY (`id`),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 14
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `match_score_project`.`player_profile`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `match_score_project`.`player_profile` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `nickname` VARCHAR(45) NOT NULL,
  `full_name` VARCHAR(45) NOT NULL,
  `country` VARCHAR(45) NOT NULL,
  `sports_club` VARCHAR(45) NULL DEFAULT NULL,
  `users_id` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `nickname_UNIQUE` (`nickname` ASC) VISIBLE,
  INDEX `fk_player_profile_users1_idx` (`users_id` ASC) VISIBLE,
  CONSTRAINT `fk_player_profile_users1`
    FOREIGN KEY (`users_id`)
    REFERENCES `match_score_project`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 25
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `match_score_project`.`link_requests`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `match_score_project`.`link_requests` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `user_id` INT(11) NOT NULL,
  `player_profile_id` INT(11) NOT NULL,
  `status` VARCHAR(10) NOT NULL DEFAULT 'pending',
  PRIMARY KEY (`id`),
  INDEX `user_id` (`user_id` ASC) VISIBLE,
  INDEX `player_profile_id` (`player_profile_id` ASC) VISIBLE,
  CONSTRAINT `link_requests_ibfk_1`
    FOREIGN KEY (`user_id`)
    REFERENCES `match_score_project`.`users` (`id`),
  CONSTRAINT `link_requests_ibfk_2`
    FOREIGN KEY (`player_profile_id`)
    REFERENCES `match_score_project`.`player_profile` (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 5
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `match_score_project`.`tournaments`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `match_score_project`.`tournaments` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(45) NOT NULL,
  `date` VARCHAR(45) NOT NULL,
  `tournament_format` VARCHAR(45) NOT NULL,
  `match_format` VARCHAR(45) NOT NULL,
  `prize` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `match_score_project`.`matches`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `match_score_project`.`matches` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `date` VARCHAR(45) NOT NULL,
  `format` VARCHAR(45) NOT NULL,
  `tournament_id` INT(11) NULL DEFAULT NULL,
  `score_1` INT(11) NULL DEFAULT NULL,
  `score_2` INT(11) NULL DEFAULT NULL,
  `player_profile_id1` INT(11) NULL DEFAULT NULL,
  `player_profile_id2` INT(11) NULL DEFAULT NULL,
  `winner` VARCHAR(45) NULL DEFAULT NULL,
  `stage` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_match_tournament1_idx` (`tournament_id` ASC) VISIBLE,
  INDEX `fk_matches_player_profile1_idx` (`player_profile_id1` ASC) VISIBLE,
  INDEX `fk_matches_player_profile2_idx` (`player_profile_id2` ASC) VISIBLE,
  CONSTRAINT `fk_match_tournament1`
    FOREIGN KEY (`tournament_id`)
    REFERENCES `match_score_project`.`tournaments` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_matches_player_profile1`
    FOREIGN KEY (`player_profile_id1`)
    REFERENCES `match_score_project`.`player_profile` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_matches_player_profile2`
    FOREIGN KEY (`player_profile_id2`)
    REFERENCES `match_score_project`.`player_profile` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 15
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `match_score_project`.`promote_requests`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `match_score_project`.`promote_requests` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `users_id` INT(11) NOT NULL,
  `status` VARCHAR(10) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_promote_requests_users1_idx` (`users_id` ASC) VISIBLE,
  CONSTRAINT `fk_promote_requests_users1`
    FOREIGN KEY (`users_id`)
    REFERENCES `match_score_project`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 2
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `match_score_project`.`tournaments_has_player_profile`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `match_score_project`.`tournaments_has_player_profile` (
  `tournaments_id` INT(11) NOT NULL,
  `player_profile_id` INT(11) NOT NULL,
  PRIMARY KEY (`tournaments_id`, `player_profile_id`),
  INDEX `fk_tournaments_has_player_profile_player_profile1_idx` (`player_profile_id` ASC) VISIBLE,
  INDEX `fk_tournaments_has_player_profile_tournaments1_idx` (`tournaments_id` ASC) VISIBLE,
  CONSTRAINT `fk_tournaments_has_player_profile_player_profile1`
    FOREIGN KEY (`player_profile_id`)
    REFERENCES `match_score_project`.`player_profile` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_tournaments_has_player_profile_tournaments1`
    FOREIGN KEY (`tournaments_id`)
    REFERENCES `match_score_project`.`tournaments` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
