<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class VotesSchools_2014 extends Model
{
    use HasFactory;
    protected $table = 'votes_schools_2014';
    protected $primaryKey = 'NM_VOTAVEL';
    public $incrementing = false;
    protected $keyType = 'string';



    public function candidate()
    {
        //$this->belongsTo(Candidate::class,'NR_CANDIDATE','NM_VOTAVEL')//owner key?
        $this->belongsTo(Candidate::class,'NM_URNA_CANDIDATO','NM_VOTAVEL')//owner key?
        ->select('ANO_ELEICAO','NM_CANDIDATO','NM_URNA_CANDIDATO','SG_UF','NM_UE','NR_CPF_CANDIDATO','CD_ELEICAO','NR_CANDIDATO');
    }

    public function getRouteKeyName()
    {
        return 'NM_VOTAVEL';
    }
}
