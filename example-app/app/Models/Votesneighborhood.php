<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Votesneighborhood extends Model
{
    use HasFactory;
    protected $table = 'votes_neighborhoods_2020';
    protected $primaryKey = 'NM_VOTAVEL';
    public $incrementing = false;
    protected $keyType = 'string';



    public function candidate()
    {
        $this->belongsTo(Candidate::class,'NM_URNA_CANDIDATO','NM_VOTAVEL')//owner key?
        ->select('ANO_ELEICAO','NM_CANDIDATO','NM_URNA_CANDIDATO','SG_UF','NM_UE','NR_CPF_CANDIDATO','CD_ELEICAO','NR_CANDIDATO');
    }

    public function getRouteKeyName()
    {
        return 'NM_VOTAVEL';
    }
}
