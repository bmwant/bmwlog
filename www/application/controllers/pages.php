<?php

class Pages extends CI_Controller {

    public function __construct() {
        parent::__construct();
    }

    public function administration() {
        $data['title'] = 'Administration';
        $data['linkid'] = 'admlink';
        $this->load->view('templates/header', $data);
        $this->load->view('administration');
        $this->load->view('templates/footer');
    }

    public function about() {
        //$data['title'] = 'About';
        //$data['linkid'] = 'abtlink';
        //$this->load->view('templates/header', $data);
        $this->load->view('jquery');
        //$this->load->view('templates/footer');
    }

    public function categories() {
        $data['title'] = 'Categories';
        $data['linkid'] = 'catlink';
        $this->load->view('templates/header', $data);
        $this->load->view('categories');
        $this->load->view('templates/footer');
    }

}
