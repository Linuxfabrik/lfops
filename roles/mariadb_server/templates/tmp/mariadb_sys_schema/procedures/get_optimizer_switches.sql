DROP PROCEDURE IF EXISTS get_optimizer_switches;

DELIMITER $$

CREATE DEFINER='root'@'localhost' PROCEDURE get_optimizer_switches(
    )
    COMMENT '
             Description
             -----------

             Shows MariaDB Optimizer Switches in tabular form.

             Parameters
             -----------

             none

             Example
             -----------

             SQL> CALL sys.get_optimizer_switches();
             +---------------------------------+-------+
             | switch_name                     | value |
             +---------------------------------+-------+
             | index_merge                     | on    |
             | index_merge_union               | on    |
             | index_merge_sort_union          | on    |
             | index_merge_intersection        | on    |
             | index_merge_sort_intersection   | off   |
             | engine_condition_pushdown       | off   |
             | index_condition_pushdown        | on    |
             | derived_merge                   | on    |
             | derived_with_keys               | on    |
             | firstmatch                      | on    |
             | loosescan                       | on    |
             | materialization                 | on    |
             | in_to_exists                    | on    |
             | semijoin                        | on    |
             | partial_match_rowid_merge       | on    |
             | partial_match_table_scan        | on    |
             | subquery_cache                  | on    |
             | mrr                             | off   |
             | mrr_cost_based                  | off   |
             | mrr_sort_keys                   | off   |
             | outer_join_with_cache           | on    |
             | semijoin_with_cache             | on    |
             | join_cache_incremental          | on    |
             | join_cache_hashed               | on    |
             | join_cache_bka                  | on    |
             | optimize_join_buffer_size       | on    |
             | table_elimination               | on    |
             | extended_keys                   | on    |
             | exists_to_in                    | on    |
             | orderby_uses_equalities         | on    |
             | condition_pushdown_for_derived  | on    |
             | split_materialized              | on    |
             | condition_pushdown_for_subquery | on    |
             | rowid_filter                    | on    |
             | condition_pushdown_from_having  | on    |
             +---------------------------------+-------+
             35 rows in set (0.153 sec)
             
             Query OK, 35 rows affected (0.191 sec)
            '
    SQL SECURITY INVOKER
    NOT DETERMINISTIC
    READS SQL DATA
BEGIN
    DECLARE v_i INT DEFAULT 1;
    DECLARE v_n INT DEFAULT 1;
  
    CREATE TEMPORARY TABLE IF NOT EXISTS `optimizer_switch_tmp` (`switch_name` VARCHAR(64), `value` VARCHAR(3));

    WHILE v_i < LENGTH(@@optimizer_switch) AND v_n != 0 DO
        SET v_n = LOCATE(',', SUBSTRING(@@optimizer_switch FROM v_i));
        IF v_n = 0 THEN
            SET v_n = LENGTH(@@optimizer_switch) - v_i+2;
        END IF;
        INSERT INTO optimizer_switch_tmp VALUES (
          SUBSTRING_INDEX(SUBSTRING(@@optimizer_switch FROM v_i FOR v_n-1), '=', 1), 
          SUBSTRING_INDEX(SUBSTRING(@@optimizer_switch FROM v_i FOR v_n-1), '=', -1)
       );
      SET v_i = v_i + v_n;
    END WHILE;
  
    SELECT * FROM optimizer_switch_tmp;
    DROP TEMPORARY TABLE optimizer_switch_tmp;
END;
$$

DELIMITER ;
