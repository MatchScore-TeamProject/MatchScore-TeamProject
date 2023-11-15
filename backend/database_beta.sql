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
-- Table `match_score_project`.`tournaments`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `match_score_project`.`tournaments` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `participants` VARCHAR(45) NOT NULL,
  `title` VARCHAR(45) NOT NULL,
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
  `participants` VARCHAR(45) NOT NULL,
  `timestamp` DATETIME NOT NULL,
  `time_limit` INT(11) NULL DEFAULT NULL,
  `score_limit` INT(11) NULL DEFAULT NULL,
  `duration` INT(11) NOT NULL,
  `score` INT(11) NULL DEFAULT NULL,
  `tournament_id` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_match_tournament1_idx` (`tournament_id` ASC) VISIBLE,
  CONSTRAINT `fk_match_tournament1`
    FOREIGN KEY (`tournament_id`)
    REFERENCES `match_score_project`.`tournaments` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `match_score_project`.`player_profile`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `match_score_project`.`player_profile` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `full_name` VARCHAR(45) NOT NULL,
  `country` VARCHAR(45) NOT NULL,
  `sports_club` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `match_score_project`.`matches_has_player_profile`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `match_score_project`.`matches_has_player_profile` (
  `matches_id` INT(11) NOT NULL,
  `player_profile_id` INT(11) NOT NULL,
  PRIMARY KEY (`matches_id`, `player_profile_id`),
  INDEX `fk_matches_has_player_profile_player_profile1_idx` (`player_profile_id` ASC) VISIBLE,
  INDEX `fk_matches_has_player_profile_matches1_idx` (`matches_id` ASC) VISIBLE,
  CONSTRAINT `fk_matches_has_player_profile_matches1`
    FOREIGN KEY (`matches_id`)
    REFERENCES `match_score_project`.`matches` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_matches_has_player_profile_player_profile1`
    FOREIGN KEY (`player_profile_id`)
    REFERENCES `match_score_project`.`player_profile` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `match_score_project`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `match_score_project`.`users` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(45) NOT NULL,
  `password` VARCHAR(99) NOT NULL,
  `player_profile_id` INT(11) NULL DEFAULT NULL,
  `user_type` VARCHAR(45) NOT NULL DEFAULT 'user',
  PRIMARY KEY (`id`),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE,
  INDEX `fk_users_player_profile1_idx` (`player_profile_id` ASC) VISIBLE,
  CONSTRAINT `fk_users_player_profile1`
    FOREIGN KEY (`player_profile_id`)
    REFERENCES `match_score_project`.`player_profile` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
