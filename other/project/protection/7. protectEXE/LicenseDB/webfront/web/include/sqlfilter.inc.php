<?php

/**
 * Filtering sql input.
 * @created: Thursday, July 15, 2010
 */
class SqlFilter{
    private $src = '';
    private $len = 0;
    private $pos = 0;
    const EOF = -1;
    public $msg = array();
    public $ast = array();

    public function __construct( $sql ){
        $this->src = $sql;
        $this->len = strlen( $this->src );
        $this->pos = 0;
    }

    private function getc(){
        return $this->pos < $this->len ? $this->src[$this->pos++] : self::EOF;
    }

    private function ungetc(){
        --$this->pos;
    }

    private function err($msg){
        $this->msg[] = array( $this->pos, $msg );
    }

    private function isletter($c){
        $c = strtolower( $c );
        return $c >= 'a' && $c <= 'z';
    }

    private function isdigit($c){
        return $c >= '0' && $c <= '9';
    }

    private function sp(){
        while(true){
            $c = $this->getc();
            if( $c == ' ' ){
                continue;
            }
            elseif( $c == self::EOF ){
                break;
            }
            else{
                $this->ungetc();
                break;
            }
        }
    }

    private function word( &$text ){
        $text = '';
        $s = 0;
        while( ( $c = $this->getc() ) !== self::EOF ){
            if( $this->isletter( $c ) ){
            }
            else{
                $this->ungetc();
                break;
            }
            $text .= $c;
            $s++ ;
        }
        if( strlen( $text ) == 0 ){
            return false;
        }
        else{
            return true;
        }
    }

    private function id( &$text ){
        $text = '';
        $s = 0;
        while( ( $c = $this->getc() ) !== self::EOF ){
            if( $s == 0 ){
                if( $this->isletter( $c ) || $c == '_' ){
                }
                else{
                    $this->err( 'Invalid name start char.' );
                    return false;
                }
            }
            else{
                if( $this->isletter( $c ) || $this->isdigit( $c ) || $c == '_' ){
                }
                else{
                    $this->ungetc();
                    break;
                }
            }
            $text .= $c;
            $s++ ;
        }
        if( strlen( $text ) == 0 ){
            $this->err('Misssing identifier.');
            return false;
        }
        else{
            return true;
        }
    }

    private function oid( &$text ){
        $text = '';
        if( $this->id( $obj ) ){
            if( $this->getc() == '.' ){
                if( $this->id( $field ) ){
                    $text = $obj . '.' .$field;
                    return true;
                }
            }
            else{
                $this->ungetc();
                $text = $obj;
                return true;
            }
        }
        return false;
    }

    private function op( &$text ){
        $text = '';
        $s = 0;
        while( $s >= 0 && ( $c = $this->getc() ) !== self::EOF ){
            switch( $c ){
                case '=':
                    $s = -2;
                    break;
                case '>':
                    $s = 100;
                    break;
                case '<':
                    $s = 200;
                    break;
                case '!':
                    $s = 300;
                    break;
                default:
                    if( strtolower( $c ) == 'i' && $s == 0 ){
                        $s = 400;
                    }
                    elseif( strtolower( $c ) == 's' && $s == 401 ){
                        $s = -2;
                    }
                    elseif( $s == 101 || $s == 201 ){
                        $this->ungetc();
                        $c = '';
                        $s = -2;
                    }
                    else{

                        $this->err( 'Invalid operator.' );
                        return false;
                    }
                    break;
            }
            $text .= $c;
            $s ++ ;
        }
        if( strlen( $text ) == 0 ){
            $this->err('Misssing operator.');
            return false;
        }
        else{
            if( $s > 100 ){
                $this->err( 'Invalid operator.' );
                return false;
            }
            else{       
                return true;
            }
        }
    }

    /*
     * 'xxxxxx'
     * +-12345
     * null
     * not null
     * true
     * false
     */
    private function operand( &$type, &$text ){
        $text = '';
        if( $this->const_int( $num ) ){
            $type = 'number';
            $text = $num;
            return true;
        }
        elseif( $this->const_str( $str ) ){
            $type = 'string';
            $text = $str;
            return true;
        }
        elseif( $this->const_val( $val ) ){
            $type = 'literal';
            $text = $val;
            return true;
        }
        $this->err('Unknown value.');
        return false;
    }

    private function const_val( &$text ){
        $text = '';
        if( $this->word( $val ) ){
            switch( strtolower( $val ) ){
                case 'null':
                case 'true':
                case 'false':
                    $text = $val;
                    return true;
                    break;
                case 'not':
                    $this->sp();
                    if( $this->word( $val2 ) ){
                        switch( strtolower( $val2 ) ){
                            case 'null':
                                $text = $val. ' '. $val2;
                                return true;
                                break;
                            default:
                                $this->err('Unsupported value.');
                                return false;
                                break;
                        }
                    }
                    else{
                        return false;
                    }
                    break;
            }
        }
        else{
            return false;
        }
    }

    private function const_str( &$text ){
        $text = '';
        $s = 0;
        $q = false;
        while( ( $c = $this->getc() ) !== self::EOF ){
            if( $c == "'" ){
                if( $s == 0 ){
                    $s ++;
                    $q = true;
                    continue;
                }
                else{
                    break;
                }
            }
            else{
                if( !$q ){
                    $this->ungetc();
                    return false;
                }
                if( $this->isletter( $c ) ){
                }
                elseif( $this->isdigit( $c ) ){
                }
                else{
                    switch( $c ){
                        case '_':
                        case '-':
                        case ' ':
                        case ':':
                        case '@':
                        case '.':
                        case '%':
                            break;
                        default:
                            return false;
                            break;
                    }
                }
            }
            $text .= $c;
            $s ++;
        }
        if( strlen( $text ) == 0 ){
            return false;
        }
        else{
            return true;
        }
    }

    private function const_int( &$text ){
        $text = '';
        $s = 0;
        while( ( $c = $this->getc() ) !== self::EOF ){
            if( $s == 0 && ( $c == '+' || $c == '-' ) ){

            }
            else{
                if( $this->isdigit( $c ) ){
                }
                else{
                    $this->ungetc();
                    break;
                }
            }
            $text .= $c;
            $s ++;
        }
        if( strlen( $text ) == 0 ){
            return false;
        }
        else{
            return true;
        }
    }

    private function cop( &$text ){
        $text = '';
        if( $this->word( $op ) ){
            switch( strtolower( $op ) ){
                case 'and':
                case 'or':
                    $text = $op;
                    return true;
                default:
                    $this->err('Unknown clause operator: '.$op.'.');
                    return false;
            }
        }
        else{
            if( $this->getc() == self::EOF ){
                return false;
            }
            else{
                $this->err('Invalid clause operator.');
                return false;
            }
        }
    }

    private function stmt( &$cl, $j='' ){
        $this->sp();
        if( !$this->oid($id) ) return false;
        $this->sp();
        if( !$this->op($op) ) return false;
        $this->sp();
        if( !$this->operand($type, $operand) ) return false;
        $this->sp();
        $cl[] = array( 'join'=>$j, 'id'=>$id, 'op'=>$op, 'valType'=>$type, 'val'=>$operand );
        return true;
    }

    private function stmts( &$cl ){
         if( !$this->stmt( $cl ) ) return false;
         while( $this->cop( $cop ) ){
             if( !$this->stmt( $cl, $cop ) ) return false;
         }
         return count( $this->msg ) == 0;
    }

    public function parse(){
        return $this->stmts( $this->ast );
    }

    private static $inst = false;
    public static function is_allow( $sql, $allowId = array() ){
        if(!self::$inst){
            self::$inst = new self( $sql );
        }
        if( self::$inst->parse() ){
            if( count( $allowId ) > 0 ){
                foreach( self::$inst->ast as $cl ){
                    if( !in_array( strtolower( $cl['id'] ), $allowId ) ){
                        return false;
                    }
                }
            }
            return true;
        }
        return false;
    }
}

?>